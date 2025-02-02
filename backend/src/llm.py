import os
from abc import ABC, abstractmethod

import instructor
from pydantic import BaseModel
from tenacity import stop_after_attempt, wait_random_exponential, retry
from openai import OpenAI

from src.templates import BasePromptTemplate


class LLMInterface(ABC):
    def __init__(self, model: str):
        self.model = model

    @abstractmethod
    def get_answer(self, prompt: str, *args, kwargs):
        pass


class Gpt(LLMInterface):
    def __init__(self, model: str):
        self.model = model
        self.llm = instructor.from_openai(OpenAI(api_key=os.getenv("OPENAI_API_KEY")))

    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
    def completion_with_backoff(self, llm, **kwargs):
        return llm.chat.completions.create(**kwargs)

    def get_answer(
        self,
        prompt: BasePromptTemplate,
        formatted_instruction: BaseModel,
        *args,
        **kwargs,
    ):

        answer = self.completion_with_backoff(
            llm=self.llm,
            model=self.model,
            temperature=0,
            response_model=formatted_instruction,
            messages=[
                {
                    "role": "user",
                    "content": prompt.create_template(args, kwargs),
                },
            ],
        )
        if formatted_instruction:
            return answer.dict()
        else:
            return answer.choices[0].message.content