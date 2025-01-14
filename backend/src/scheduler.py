import json
import os
import time
import uuid

import backoff
import httpx
import openai
from openai import OpenAI

from db import database
from llm import Gpt
from schemas import TrendReportResponse
from templates import TrendReportTemplate


@backoff.on_exception(backoff.expo, openai.RateLimitError)
def completion_with_backoff(llm, **kwargs):
    return llm.chat.completions.create(**kwargs)


# def create_report_for_batch(batch):
#     print("Starting report creation for batch.")
#
#     llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
#     model = os.getenv('OPENAI_MODEL', default="gpt-4o-mini")
#
#     print(f"Requesting initial completion with batch data: {batch}")
#
#     posts = " ".join([f"{n + 1}. {p.get('text')}\n" for n, p in enumerate(batch)])
#
#     try:
#         response = completion_with_backoff(
#             llm=llm,
#             model=model,
#             messages=[
#                 {
#                     "role": "user",
#                     "content": TrendReportTemplate().create_template(posts),
#                 },
#             ],
#         )
#     except Exception as e:
#         print("Failed during GPT call:", e)
#         raise e
#
#     # Extract the response text
#     return response.choices[0].message.content

    # print("Received report text from GPT:")
    # print(report_text)


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

    return {
        "statusCode": 200,
        "body": response
    }
