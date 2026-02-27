from __future__ import annotations

import re

STANDARD_HEADINGS = {
    "summary",
    "experience",
    "education",
    "skills",
    "projects",
    "certifications",
}

ICON_RE = re.compile(r"[\U0001F300-\U0001FAFF\u2600-\u27BF]")
TABLE_HINT_RE = re.compile(r"\|.+\||\t{2,}| {8,}")
FANCY_FONT_HINT_RE = re.compile(r"[𝒜-𝓏𝔄-𝔷𝕬-𝖟]")


def evaluate_ats_hard_rules(resume_text: str) -> tuple[int, list[str], list[str]]:
    checks = {
        "single_column_layout": _single_column(resume_text),
        "no_tables": not bool(TABLE_HINT_RE.search(resume_text)),
        "no_icons_images": not bool(ICON_RE.search(resume_text)),
        "standard_headings": _has_standard_headings(resume_text),
        "bullet_points": _has_bullets(resume_text),
        "font_compatibility": not bool(FANCY_FONT_HINT_RE.search(resume_text)),
    }

    weight = 10
    score = sum(weight for passed in checks.values() if passed)
    failed_reasons = [name for name, passed in checks.items() if not passed]
    fixes = [_rule_fix(reason) for reason in failed_reasons]
    return score, failed_reasons, fixes


def _single_column(text: str) -> bool:
    lines = text.splitlines()
    suspicious = sum(1 for line in lines if "   " in line and len(line) > 70)
    return suspicious < 3


def _has_standard_headings(text: str) -> bool:
    lowered = {line.strip().strip(":").lower() for line in text.splitlines() if line.strip()}
    return len(lowered.intersection(STANDARD_HEADINGS)) >= 3


def _has_bullets(text: str) -> bool:
    return any(line.strip().startswith(("-", "•", "*")) for line in text.splitlines())


def _rule_fix(reason: str) -> str:
    mapping = {
        "single_column_layout": "Use a single-column layout and avoid multi-column formatting.",
        "no_tables": "Remove table-like formatting and use plain text sections.",
        "no_icons_images": "Remove icons/emojis/images and keep text-only contact details.",
        "standard_headings": "Use standard headings such as Summary, Skills, Experience, and Education.",
        "bullet_points": "Convert dense paragraphs into concise bullet points.",
        "font_compatibility": "Use ATS-safe standard fonts and remove special Unicode glyphs.",
    }
    return mapping[reason]
