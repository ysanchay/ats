from __future__ import annotations

import io
import re
from typing import Iterable

from .schemas import ExperienceItem, ParsedResume, ParsedSections

SECTION_HEADERS = {
    "summary": ["summary", "profile", "professional summary"],
    "skills": ["skills", "technical skills", "core skills"],
    "experience": ["experience", "work experience", "employment"],
    "education": ["education", "academic background"],
    "projects": ["projects", "project experience"],
}


EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE_RE = re.compile(r"(?:\+?\d{1,3}[\s.-]?)?(?:\(\d{3}\)|\d{3})[\s.-]?\d{3}[\s.-]?\d{4}")


def extract_text(filename: str, content: bytes) -> str:
    if filename.lower().endswith(".pdf"):
        return _extract_pdf(content)
    if filename.lower().endswith(".docx"):
        return _extract_docx(content)
    return content.decode("utf-8", errors="ignore")


def _extract_pdf(content: bytes) -> str:
    from pypdf import PdfReader

    reader = PdfReader(io.BytesIO(content))
    pages = [page.extract_text() or "" for page in reader.pages]
    return "\n".join(pages)


def _extract_docx(content: bytes) -> str:
    from docx import Document

    doc = Document(io.BytesIO(content))
    return "\n".join(p.text for p in doc.paragraphs)


def normalize_text(text: str) -> str:
    text = text.replace("\r", "\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def parse_resume(text: str) -> ParsedResume:
    normalized = normalize_text(text)
    lines = [line.strip() for line in normalized.splitlines() if line.strip()]

    name = lines[0] if lines else ""
    email_match = EMAIL_RE.search(normalized)
    phone_match = PHONE_RE.search(normalized)

    sections = _split_sections(lines)
    parsed_sections = ParsedSections(
        summary=" ".join(sections.get("summary", [])),
        skills=_parse_skills(sections.get("skills", [])),
        experience=_parse_experience(sections.get("experience", [])),
        education=" ".join(sections.get("education", [])),
        projects=sections.get("projects", []),
    )

    return ParsedResume(
        name=name,
        email=email_match.group(0) if email_match else "",
        phone=phone_match.group(0) if phone_match else "",
        sections=parsed_sections,
        raw_text=normalized,
    )


def _split_sections(lines: Iterable[str]) -> dict[str, list[str]]:
    current = "summary"
    section_map: dict[str, list[str]] = {k: [] for k in SECTION_HEADERS}

    for line in lines:
        lowered = line.lower().strip(":")
        for section, aliases in SECTION_HEADERS.items():
            if lowered in aliases:
                current = section
                break
        else:
            section_map[current].append(line)

    return section_map


def _parse_skills(lines: list[str]) -> list[str]:
    joined = " ".join(lines)
    tokens = re.split(r"[,|•]\s*", joined)
    return [token.strip() for token in tokens if token.strip()]


def _parse_experience(lines: list[str]) -> list[ExperienceItem]:
    blocks: list[ExperienceItem] = []
    current = ExperienceItem()

    for line in lines:
        if line.startswith(("-", "•")):
            current.bullets.append(line.lstrip("-• ").strip())
            continue

        if current.role or current.company or current.bullets:
            blocks.append(current)

        parts = [p.strip() for p in line.split("|")]
        role = parts[0] if parts else line
        company = parts[1] if len(parts) > 1 else ""
        current = ExperienceItem(role=role, company=company, bullets=[])

    if current.role or current.company or current.bullets:
        blocks.append(current)

    return blocks
