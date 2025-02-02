import json

from src.db import database
from src.gateways import RapidGateway

client = RapidGateway()


def handler(event):

    body = json.loads(event.get("body", {}))

    link = body.get('link')
    print(f"Started crawler function for: {link}")

    correlation_id = event.get('headers').get('correlation-id', "")

    try:
        posts = [{
            "text": post.get("text", "").strip(),
            "correlation_id": event.get('headers').get('correlation-id', ""),
            "urn": post.get("urn")
            } for post in client.list_posts(link)]

        existing_posts = [ep.get("urn") for ep in list(database.posts.find(
            {"urn": {"$in": [p.get("urn") for p in posts]}},
            {"urn": 1}
        ))]
    except Exception as e:
        database.finished.insert_one({"correlation_id": correlation_id})
        return

    posts = list(filter(lambda x: x["urn"] not in existing_posts, posts))

    if not posts:
        database.finished.insert_one({"correlation_id": correlation_id})
        print("No new posts on page")
        return

    try:
        results = database.posts.insert_many(posts)
    except Exception as e:
        return {
            "statusCode": 500,
            "body": str(e)
        }

    print(f"Successfully Inserted {len(results.inserted_ids)}")
    database.finished.insert_one({"correlation_id": correlation_id})

    return {
        "statusCode": 200,
        "body": f"Hello, crawler! Welcome to Genezio Functions!"
    }
