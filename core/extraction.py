"""Extract text from saved, validated PDF and TXT files (locally only)."""
from dataclasses import dataclass
from pathlib import Path
from typing import List, Union

import fitz


@dataclass(frozen=True)
class PageText:
    page_number: int
    text: str


class ExtractionError(Exception):
    def __init__(self, code: str):
        self.code = code
        super().__init__(code)


def extract_pages(file_path: Union[str, Path]) -> List[PageText]:
    """One PageText per PDF page or one for a UTF-8 TXT file.

    Call with the safe saved path produced by core.upload.validate_upload().
    For scanned PDFs without any text layer, raises NO_TEXT_LAYER.
    """
    path = Path(file_path)
    suffix = path.suffix.lower()

    if suffix == ".txt":
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            raise ExtractionError("TXT_INVALID_ENCODING") from exc
        except OSError as exc:
            raise ExtractionError("TXT_READ_ERROR") from exc
        return [PageText(page_number=1, text=text)]

    if suffix != ".pdf":
        raise ExtractionError("INVALID_FILE_TYPE")

    try:
        with fitz.open(path) as document:
            pages = [
                PageText(page_number=index, text=page.get_text("text"))
                for index, page in enumerate(document, start=1)
            ]
    except (OSError, RuntimeError, ValueError) as exc:
        raise ExtractionError("PDF_INVALID") from exc

    if not any(page.text.strip() for page in pages):
        raise ExtractionError("NO_TEXT_LAYER")

    return pages
