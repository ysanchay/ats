from app.ats_rules import evaluate_ats_hard_rules
from app.keywords import keyword_match
from app.parser import parse_resume
from app.services import run_ats_checker


def test_parser_extracts_contact():
    text = """Jane Doe
jane@doe.com | 555-123-4567
Skills
Python, SQL
Experience
Engineer | Acme
- Built ETL pipelines
"""
    parsed = parse_resume(text)
    assert parsed.email == "jane@doe.com"
    assert parsed.phone == "555-123-4567"
    assert "Python" in parsed.sections.skills


def test_ats_rules_detect_icons_and_tables():
    text = "Experience | Skills\n😀"
    score, failed, _ = evaluate_ats_hard_rules(text)
    assert score < 60
    assert "no_icons_images" in failed


def test_keyword_match_basics():
    resume = "Python SQL FastAPI ETL"
    jd = "Looking for Python SQL dbt airflow"
    result = keyword_match(resume, jd)
    assert "python" in result["matched_keywords"]
    assert "airflow" in result["missing_keywords"]


def test_ats_checker_returns_score_range():
    resume = """Alex Roe
alex@roe.com
Experience
- Built data pipelines in Python and SQL.
"""
    jd = "Need python sql airflow"
    result = run_ats_checker(resume, jd)
    assert 0 <= result.ats_score <= 100


def test_ats_checker_flags_table_spacing_in_resume_text():
    resume = """Jordan Lane
jordan@lane.com
Experience        Skills
- Built data pipelines in Python.
"""
    result = run_ats_checker(resume, "Need python")
    assert "no_tables" in result.rejection_reasons


def test_parser_preserves_layout_signals_for_ats_checks():
    text = """Jordan Lane
jordan@lane.com
Experience\t\tSkills
Role        Company
"""
    parsed = parse_resume(text)
    assert "\t\t" in parsed.raw_text
    assert "        " in parsed.raw_text
