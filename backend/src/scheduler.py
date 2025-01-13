import concurrent
import concurrent.futures
import os
from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta, datetime

import backoff
import openai
from openai import OpenAI

from src.db import database
from src.templates import TrendReportTemplate


@backoff.on_exception(backoff.expo, openai.RateLimitError)
def completion_with_backoff(llm, **kwargs):
    return llm.chat.completions.create(**kwargs)


def create_report_for_batch(batch):
    print("Starting report creation for batch.")

    llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    model = os.getenv('OPENAI_MODEL', default="gpt-4o-mini")

    print(f"Requesting initial completion with batch data: {batch}")

    posts = " ".join([f"{n + 1}. {p.get('text')}\n" for n, p in enumerate(batch)])

    prompt = TrendReportTemplate().create_template(posts)
    print(prompt)
    try:
        response = completion_with_backoff(
            llm=llm,
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": TrendReportTemplate().create_template(posts),
                },
            ],
        )
    except Exception as e:
        print("Failed during GPT call:", e)
        raise e

    # Extract the response text
    report_text = response.choices[0].message.content
    print("Received report text from GPT:")
    print(report_text)


def generate_profiles_report(posts: list[dict]) -> list[str]:
    """
    Method that creates a chain to output a profile report based on the scraped data.
    :returns: list of reports
    """

    responses = []
    input_var = [f"{p.get('content')} {p.get('link')} {p.get('name')} \n" for p in posts]

    batch_size = 50

    # create batches
    batches = [
        input_var[i: i + batch_size] for i in range(0, len(input_var), batch_size)
    ]

    with ThreadPoolExecutor(max_workers=12) as executor:
        future_to_batch = {
            executor.submit(create_report_for_batch, batch): batch
            for batch in batches
        }
        for future in concurrent.futures.as_completed(future_to_batch):
            batch_result = future.result()
            responses.append(batch_result)

    return responses


def handler(event):
    body = event.get("body", {})

    # for _ in range(4):
    #     response = httpx.post(
    #         "http://localhost:8083/.functions/function-crawler",
    #         json={"link": "https://www.instagram.com/mcdonalds/"},
    #         headers={"Content-Type": "application/json", "Correlation-ID": str(uuid.uuid4())},
    #     )

    now = datetime.now()
    posts = list(
        database.profiles.find(
            {
                "date": {"$gte": (now - timedelta(days=7)), "$lte": now},
            }
        )
    )

    print(f"Gathered {len(posts)} posts")

    if not posts:
        print("Cannot generate report, no new posts available")
        return

    reports = generate_profiles_report(posts)

    return {
        "statusCode": 200,
        "body": f"Hello, scheduler! Welcome to Genezio Functions!"
    }