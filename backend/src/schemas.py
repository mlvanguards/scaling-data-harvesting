from typing import List

from pydantic import BaseModel, Field


class TrendItem(BaseModel):
    """
    Represents one major trend, including the rationale (why)
    and recommendation for action.
    """
    title: str = Field(..., description="Title or main focus of the trend")
    why: str = Field(..., description="Explanation of why the trend matters")
    recommendation: str = Field(..., description="Recommendation based on the trend")


class TrendReportResponse(BaseModel):
    """
    Overall report capturing multiple trends and a summary.
    """
    trends: List[TrendItem] = Field(
        ...,
        description="List of identified trends with their 'why' and 'recommendation' insights.",
    )
    summary_of_findings: str = Field(
        ...,
        description="Consolidated summary or conclusion derived from the trends."
    )