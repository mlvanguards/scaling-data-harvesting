import concurrent
import os
import time
import uuid
from datetime import timedelta, datetime

import httpx

import backoff
import openai
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from openai import OpenAI


from src.db import database
from src.scheduler import create_report_for_batch

posts = list(database.posts.find())

print(create_report_for_batch(posts))
# prepared_posts = " ".join([f"{n + 1}. {p.get('text')}\n" for n, p in enumerate(posts)])
#
# prepared_posts

