from __future__ import annotations

import re
from collections import Counter

STOPWORDS = {
    "and",
    "the",
    "with",
    "for",
    "you",
    "your",
    "our",
    "are",
    "this",
    "that",
    "from",
    "into",
    "will",
    "years",
    "experience",
    "team",
    "role",
    "job",
}


def tokenize(text: str) -> list[str]:
    tokens = re.findall(r"[a-zA-Z][a-zA-Z0-9+#.-]{1,}", text.lower())
    return [t for t in tokens if t not in STOPWORDS and len(t) > 2]


def extract_keywords(job_description: str, top_n: int = 30) -> list[str]:
    freq = Counter(tokenize(job_description))
    return [kw for kw, _ in freq.most_common(top_n)]


def keyword_match(resume_text: str, job_description: str) -> dict[str, object]:
    jd_keywords = extract_keywords(job_description)
    if not jd_keywords:
        return {
            "matched_keywords": [],
            "missing_keywords": [],
            "weak_keywords": [],
            "match_percentage": 0,
        }

    resume_tokens = Counter(tokenize(resume_text))
    matched = [kw for kw in jd_keywords if kw in resume_tokens]
    weak = [kw for kw in matched if resume_tokens[kw] == 1]
    missing = [kw for kw in jd_keywords if kw not in resume_tokens]
    match_pct = int((len(matched) / len(jd_keywords)) * 100)

    return {
        "matched_keywords": matched,
        "missing_keywords": missing,
        "weak_keywords": weak,
        "match_percentage": match_pct,
    }
