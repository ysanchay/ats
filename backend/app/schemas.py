from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ExperienceItem:
    role: str = ""
    company: str = ""
    bullets: list[str] = field(default_factory=list)


@dataclass
class ParsedSections:
    summary: str = ""
    skills: list[str] = field(default_factory=list)
    experience: list[ExperienceItem] = field(default_factory=list)
    education: str = ""
    projects: list[str] = field(default_factory=list)


@dataclass
class ParsedResume:
    name: str = ""
    email: str = ""
    phone: str = ""
    sections: ParsedSections = field(default_factory=ParsedSections)
    raw_text: str = ""


@dataclass
class ResumeRequest:
    resume_text: str
    job_description: str = ""
    target_role: str = ""


@dataclass
class AtsBreakdown:
    format: int
    keywords: int
    clarity: int


@dataclass
class AtsScoreResponse:
    ats_score: int
    breakdown: AtsBreakdown
    rejection_reasons: list[str]
    fixes: list[str]


@dataclass
class KeywordResponse:
    missing_keywords: list[str]
    weak_keywords: list[str]
    suggested_bullets: list[str]
    matched_keywords: list[str]
    match_percentage: int


@dataclass
class OnePageResponse:
    condensed_resume_text: str
    removed_sections_summary: list[str]
    final_word_count: int
