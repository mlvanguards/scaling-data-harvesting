import json
import os
import time
import uuid

import backoff
import httpx
import openai

from src.db import database
from src.llm import Gpt
from src.schemas import TrendReportResponse
from src.templates import TrendReportTemplate


@backoff.on_exception(backoff.expo, openai.RateLimitError)
def completion_with_backoff(llm, **kwargs):
    return llm.chat.completions.create(**kwargs)


def handler(event):
    body = json.loads(event.get("body", {}))

    correlation_ids = []

    for link in body.get("links", []):
        correlation_id = str(uuid.uuid4())
        try:
            response = httpx.post(
                os.getenv("CRAWLER_URL"),
                json={"link": link},
                headers={"Content-Type": "application/json", "Correlation-ID": correlation_id},
            )
        except Exception as e:
            continue

        print(f"Started watching crawler with id: {correlation_id}")
        correlation_ids.append(correlation_id)

    while True:
        finished = list(database.finished.find({"correlation_id": {"$in": correlation_ids}}))
        for c in finished:
            correlation_ids.remove(c.get("correlation_id"))

        if not correlation_ids:
            database.finished.delete_many({})
            break

        print(f"Still waiting for {len(correlation_ids)} crawlers to finish")
        time.sleep(2)

    posts = list(database.posts.find({}))
    print(f"Gathered {len(posts)} posts")

    if not posts:
        print("Cannot generate report, no new posts available")
        return

    llm = Gpt(os.getenv('OPENAI_MODEL', default="gpt-4o-mini"))

    response = llm.get_answer(
        prompt=TrendReportTemplate(),
        posts=posts,
        formatted_instruction=TrendReportResponse,
    )

    print("Successfully generated report")

    return {
        "statusCode": 200,
        "body": response
    }
