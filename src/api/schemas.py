from typing import Literal

class QueryRequest(BaseModel):
    question: str
    user_id: Optional[str]
    lang: Optional[Literal["en", "hi", "or"]] = "en"  # "hi"=Hindi, "or"=Odia

# In routes.py
from ..utils.translation import translate_to_english, translate_from_english

@router.post("/query", response_model=QueryResponse)
def query(req: QueryRequest):
    t0 = time.time()
    try:
        q_eng = translate_to_english(req.question, req.lang)
        answer, sources = answer_question(q_eng, collection)
        answer_out = translate_from_english(answer, req.lang)
        return QueryResponse(
            answer=answer_out,
            sources=sources,
            confidence=0.95,
            response_time_ms=int((time.time()-t0)*1000)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class FeedbackRequest(BaseModel):
    question: str
    answer: str
    feedback: str
    user_id: Optional[str] = None
