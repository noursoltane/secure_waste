from pathlib import Path

import fitz
import pytest

from core.extraction import ExtractionError, PageText, extract_pages

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture(scope="module", autouse=True)
def generated_fixtures():
    from scripts.make_fixtures import make_fixtures
    make_fixtures()


def test_pdf_three_pages():
    pages = extract_pages(FIXTURES / "three_page_invoice.pdf")
    assert len(pages) == 3
    assert [p.page_number for p in pages] == [1, 2, 3]
    assert all(isinstance(p, PageText) for p in pages)
    assert "DEMO-2026-001" in pages[0].text
    assert "900.00 TND" in pages[1].text
    assert "salary" in pages[2].text.lower()


def test_txt_one_page():
    pages = extract_pages(FIXTURES / "synthetic_records.txt")
    assert len(pages) == 1
    assert pages[0].page_number == 1
    assert "jamie@example.invalid" in pages[0].text


def test_pdf_without_text_layer():
    with pytest.raises(ExtractionError, match="NO_TEXT_LAYER"):
        extract_pages(FIXTURES / "image_only.pdf")


def test_blank_pdf_page_retained(tmp_path):
    document = fitz.open()
    document.new_page()
    document.new_page().insert_text((40, 40), "Visible text")
    path = tmp_path / "mixed.pdf"
    document.save(path)
    document.close()
    pages = extract_pages(path)
    assert len(pages) == 2
    assert pages[0].text.strip() == ""
    assert "Visible text" in pages[1].text


def test_reject_unsupported_file(tmp_path):
    path = tmp_path / "test.exe"
    path.write_text("text")
    with pytest.raises(ExtractionError, match="INVALID_FILE_TYPE"):
        extract_pages(path)
