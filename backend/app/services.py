from __future__ import annotations

from .ats_rules import evaluate_ats_hard_rules
from .keywords import keyword_match
from .parser import parse_resume
from .schemas import AtsBreakdown, AtsScoreResponse, KeywordResponse, OnePageResponse


def run_ats_checker(resume_text: str, job_description: str) -> AtsScoreResponse:
    parsed = parse_resume(resume_text)
    rule_score, failed_reasons, fixes = evaluate_ats_hard_rules(parsed.raw_text)
    kw = keyword_match(parsed.raw_text, job_description)

    format_score = min(40, int((rule_score / 60) * 40))
    keyword_score = min(40, int((kw["match_percentage"] / 100) * 40))
    clarity_score = _clarity_score(parsed.raw_text)

    total = format_score + keyword_score + clarity_score
    rejection_reasons = failed_reasons[:5]

    if not job_description:
        fixes.append("Add a job description to improve keyword relevance scoring.")

    return AtsScoreResponse(
        ats_score=total,
        breakdown=AtsBreakdown(format=format_score, keywords=keyword_score, clarity=clarity_score),
        rejection_reasons=rejection_reasons,
        fixes=fixes[:5],
    )


def run_keyword_optimizer(resume_text: str, job_description: str) -> KeywordResponse:
    kw = keyword_match(resume_text, job_description)
    bullets = [
        f"Integrated {missing} into project deliverables with measurable impact."
        for missing in kw["missing_keywords"][:5]
    ]
    return KeywordResponse(
        missing_keywords=kw["missing_keywords"],
        weak_keywords=kw["weak_keywords"],
        suggested_bullets=bullets,
        matched_keywords=kw["matched_keywords"],
        match_percentage=kw["match_percentage"],
    )


def run_one_page(resume_text: str) -> OnePageResponse:
    lines = [line.strip() for line in resume_text.splitlines() if line.strip()]
    kept: list[str] = []
    removed: list[str] = []

    for line in lines:
        if len(kept) > 80:
            removed.append(line)
            continue
        if line.lower() in {"references", "hobbies", "interests"}:
            removed.append(f"Removed section heading: {line}")
            continue
        kept.append(line)

    condensed = "\n".join(kept)
    words = len(condensed.split())

    if words > 600:
        trimmed = condensed.split()
        condensed = " ".join(trimmed[:600])
        words = 600
        removed.append("Trimmed content to 600 words.")

    return OnePageResponse(
        condensed_resume_text=condensed,
        removed_sections_summary=removed[:20],
        final_word_count=words,
    )


def _clarity_score(text: str) -> int:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    long_lines = sum(1 for line in lines if len(line) > 140)
    bullet_lines = sum(1 for line in lines if line.startswith(("-", "•", "*")))

    score = 20
    if long_lines > 4:
        score -= 6
    if bullet_lines < 3:
        score -= 6
    if len(lines) < 8:
        score -= 4

    return max(0, score)
