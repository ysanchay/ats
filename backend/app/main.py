from __future__ import annotations

from fastapi import FastAPI

from .schemas import AtsScoreResponse, KeywordResponse, OnePageResponse, ResumeRequest
from .services import run_ats_checker, run_keyword_optimizer, run_one_page

app = FastAPI(title="ResumeScan Pro API", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/resume-ats-checker", response_model=AtsScoreResponse)
def resume_ats_checker(payload: ResumeRequest) -> AtsScoreResponse:
    return run_ats_checker(payload.resume_text, payload.job_description)


@app.post("/resume-keyword-optimizer", response_model=KeywordResponse)
def resume_keyword_optimizer(payload: ResumeRequest) -> KeywordResponse:
    return run_keyword_optimizer(payload.resume_text, payload.job_description)


@app.post("/resume-one-page", response_model=OnePageResponse)
def resume_one_page(payload: ResumeRequest) -> OnePageResponse:
    return run_one_page(payload.resume_text)
