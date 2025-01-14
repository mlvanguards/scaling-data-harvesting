import os

from src.db import database
from src.llm import Gpt
from src.schemas import TrendReportResponse
from src.templates import TrendReportTemplate

posts = list(database.posts.find())

# print(create_report_for_batch(posts))
# prepared_posts = " ".join([f"{n + 1}. {p.get('text')}\n" for n, p in enumerate(posts)])
#
# prepared_posts
print(len(posts))
llm = Gpt(os.getenv('OPENAI_MODEL', default="gpt-4o-mini"))

response = llm.get_answer(
    prompt=TrendReportTemplate(),
    posts=posts,
    formatted_instruction=TrendReportResponse,
)

print(response)
