from typing import List
from pydantic import BaseModel

class AnswerRequest(BaseModel):
    question: str
    stockId: str
    userId: str
    role: str

class SummaryCard(BaseModel):
    type: str
    title: str
    content: str

class AnswerResponse(BaseModel):
    logs: List[str]
    summaryCards: List[SummaryCard] 