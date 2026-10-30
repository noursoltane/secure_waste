"""End-to-end tests for upload validation and local extraction."""
import io

import pytest

from core.extraction import extract_pages
from core.upload import validate_upload
from scripts.make_fixtures import make_fixtures, FIXTURES


class FakeFile:
    def __init__(self, filename, content):
        self.filename = filename
        self.stream = io.BytesIO(content)


@pytest.fixture(scope="module", autouse=True)
def fixtures():
    make_fixtures()


@pytest.mark.parametrize("filename", ["three_page_invoice.pdf", "synthetic_records.txt"])
def test_validated_upload_passes_to_extraction(tmp_path, filename):
    validated = validate_upload(
        FakeFile(filename, (FIXTURES / filename).read_bytes())
    )
    path = tmp_path / validated["filename"]
    path.write_bytes(validated["content"])
    pages = extract_pages(path)
    assert len(pages) == (3 if filename.endswith(".pdf") else 1)
    assert all(isinstance(page.text, str) for page in pages)
