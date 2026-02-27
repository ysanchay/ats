# ResumeScan Pro (MVP Backend)

This repository contains an initial implementation of the **ResumeScan Pro** backend described in the product brief:

- `/resume-ats-checker`
- `/resume-keyword-optimizer`
- `/resume-one-page`

## Stack

- FastAPI backend
- Rule-based ATS engine (non-LLM)
- Hybrid keyword matcher
- LLM prompt templates with strict JSON schemas

## Quick start

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## API Endpoints

- `POST /resume-ats-checker`
- `POST /resume-keyword-optimizer`
- `POST /resume-one-page`

All endpoints accept normalized resume text and optional JD/target role fields.

## Notes

- Parser supports `.pdf`, `.docx`, and plain text uploads.
- Privacy-by-design hooks are included (ephemeral processing, no persistence layer).
- LLM calls are intentionally separated behind prompt builders to keep ATS hard rules deterministic.
