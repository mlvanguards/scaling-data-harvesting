import asyncio
import json
from datetime import timedelta, datetime

from crawlers import dispatcher
from db import database
from gateways import RapidGateway
from utils import clean_text

client = RapidGateway()


async def main(event):

    body = json.loads(event.get("body", {}))

    link = body.get('link')

    posts = [{
        "text": clean_text(post.get("text")).strip(),
        "correlation_id": event.get('headers').get('correlation-id', ""),
        "urn": post.get("urn")
        } for post in client.list_posts(link)]

    existing_posts = [ep.get("urn") for ep in list(database.posts.find(
        {"urn": {"$in": [p.get("urn") for p in posts]}},
        {"urn": 1}
    ))]

    posts = list(filter(lambda x: x["urn"] not in existing_posts, posts))

    if not posts:
        print("No new posts on page")
        return

    print(f"Successfully extracted {len(posts)} posts")
    try:
        results = database.posts.insert_many(posts)
    except Exception as e:
        return {
            "statusCode": 500,
            "body": str(e)
        }

    print(f"Successfully Inserted {len(results.inserted_ids)}")


def handler(event):
    result = asyncio.run(main(event))

    return {
        "statusCode": 200,
        "body": f"Hello, crawler! Welcome to Genezio Functions!"
    }
