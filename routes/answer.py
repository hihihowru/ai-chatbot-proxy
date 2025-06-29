from fastapi import APIRouter
from ..schemas import AnswerRequest, AnswerResponse
from ..utils.log_generator import generate_logs
from ..llm.summarizer import summarize_with_llm

router = APIRouter()

@router.post("/answer", response_model=AnswerResponse)
async def answer(req: AnswerRequest):
    logs = list(generate_logs())
    summary_cards = summarize_with_llm(req.question, req.stockId, req.role)
    return AnswerResponse(
        logs=logs,
        summaryCards=summary_cards
    ) 