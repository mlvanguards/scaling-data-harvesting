from abc import abstractmethod, ABC
from pydantic import BaseModel


class BasePromptTemplate(ABC, BaseModel):
    @abstractmethod
    def create_template(self, *args) -> str:
        pass


class TrendReportTemplate(BasePromptTemplate):
    prompt: str = """
    # GOAL:
    You are a market research and trend analysis expert who specializes in detecting emerging technology trends from LinkedIn posts.
    You will analyze text to identify repeated keywords, measure sentiment, and provide actionable insights.
    
    # TASKS:
    1. Identify repeated keywords and technology topics across all provided posts.
    2. Assess sentiment (positive, negative, or neutral) around each major topic.
    3. Determine which trends are emerging or rapidly growing.
    4. Provide context or possible reasons for each trend’s growth.
    5. Suggest how individuals or companies might leverage these trends.
    6. Conclude with a concise summary of your findings.
    
    # RETURN FORMAT:
    1. Present the analysis in bullet points or short paragraphs.
    2. Start with the top 3–5 technology trends you see.
       - Include a brief explanation of 'why' each trend is gaining momentum.
       - Include a prediction or recommendation for each trend.
    3. End with a summary paragraph wrapping up the overall insights.
    
    # WARNINGS:
    - Privacy: Do not reveal personally identifiable information of any LinkedIn user.
    - Confidentiality: Only use the text provided. Do not speculate on private details beyond what is in the text.
    - Compliance: Do not store or share the data beyond this analysis if it contains sensitive or proprietary information.
    
    # CONTEXT DUMP:
    Posts:
    {posts}
    
    """

    def create_template(self, posts: str) -> str:
        return self.prompt.format(posts=posts)
