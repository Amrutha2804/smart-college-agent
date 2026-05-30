from fastapi import APIRouter, HTTPException
from ..rag.embeddings import create_vector_db
from ..rag.chunking import chunk_kiit_docs
from ..rag.retrieval import answer_question
from .schemas import QueryRequest, QueryResponse
import time

router = APIRouter()

docs_chunks = chunk_kiit_docs("./data/kiit_docs")
collection = create_vector_db(docs_chunks)

@router.get("/health")
def health():
    return {"status": "ok"}

@router.post("/query", response_model=QueryResponse)
def query(req: QueryRequest):
    t0 = time.time()
    try:
        answer, sources = answer_question(req.question, collection)
        return QueryResponse(
            answer=answer,
            sources=sources,
            confidence=0.95,
            response_time_ms=int((time.time()-t0)*1000)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

import json

@router.post("/feedback")
def feedback(req: FeedbackRequest):
    with open("./data/feedback_log.jsonl", "a") as f:
        f.write(json.dumps(req.dict()) + "\n")
    return {"status": "ok"}
import json

@router.get("/faq")
def faq():
    with open("./data/faqs.json", "r") as f:
        data = json.load(f)
    return {"categories": list(data.keys()), "faqs": data}
