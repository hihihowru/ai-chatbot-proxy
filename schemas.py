from typing import List, Optional, Any, Dict
from pydantic import BaseModel

class AnswerRequest(BaseModel):
    question: str
    stockId: str
    userId: str
    role: str

class WatchlistRequest(BaseModel):
    stock_list: List[int]
    userId: str

class SummaryCard(BaseModel):
    type: str
    title: str
    content: str
    data: Optional[Any] = None

class Section(BaseModel):
    title: str
    content: str
    cards: List[SummaryCard]
    sources: List[dict]

class AnswerResponse(BaseModel):
    logs: List[str]
    summaryCards: List[SummaryCard]

class WatchlistResponse(BaseModel):
    success: bool
    sections: List[Section]
    logs: List[str]
    error: Optional[str] = None 