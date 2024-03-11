from typing import List

from pydantic import BaseModel, Field


class InsightsRequestSchema(BaseModel):
    interaction_url: str
    trackers: list[str]


class InsightResponseSchema(BaseModel):
    sentence_index: int
    start_word_index: int
    end_word_index: int
    tracker_value: str
    transcribe_value: str


class InsightsResponseSchema(BaseModel):
    insights: List[InsightResponseSchema] = Field(default_factory=list)
