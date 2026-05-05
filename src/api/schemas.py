from pydantic import BaseModel
from typing import List, Optional

class QueryRequest(BaseModel):
    question: str
    user_id: Optional[str]

class QueryResponse(BaseModel):
    answer: str
    sources: Optional[List[str]] = []
    confidence: Optional[float] = None
    response_time_ms: Optional[int] = None

class FeedbackRequest(BaseModel):
    question: str
    answer: str
    feedback: str
