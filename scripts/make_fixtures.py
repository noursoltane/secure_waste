"""Generate fictional PDF/TXT documents. Run: python scripts/make_fixtures.py"""
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures"


def make_fixtures() -> None:
    FIXTURES.mkdir(parents=True, exist_ok=True)
    text_pages = [
        "NORTHSTAR DEMO COMPANY\nInvoice DEMO-2026-001\nEmail: alex@example.invalid",
        "INVOICE ITEMS\nSecurity workshop: 2 units\nSubtotal: 900.00 TND",
        "PAYMENT INFORMATION\nPhone: +216 20 000 000\nFictional salary: 2,500 TND",
    ]
    document = fitz.open()
    for text in text_pages:
        page = document.new_page()
        page.insert_text((50, 80), text, fontsize=12)
    document.save(FIXTURES / "three_page_invoice.pdf")
    document.close()

    # A page with a drawn raster-independent graphic but no PDF text layer.
    document = fitz.open()
    page = document.new_page()
    page.draw_rect(fitz.Rect(70, 70, 400, 320), color=(0, 0, 0), fill=(0.7, 0.7, 0.7))
    document.save(FIXTURES / "image_only.pdf")
    document.close()

    (FIXTURES / "synthetic_records.txt").write_text(
        "Employee: Jamie Example\nEmail: jamie@example.invalid\n"
        "Phone: +216 20 000 000\nSalary: 2,500 TND (fictional)\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    make_fixtures()
    print(f"Synthetic fixtures generated: {FIXTURES}")
