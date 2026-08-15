"""Turn linkedin.pdf into the plain text that Render needs as a secret file.

Render secret files are plain text, so the binary PDF can't be uploaded as-is.
Run this locally, then paste the output into a Render secret file named
`linkedin.txt`:

    uv run python extract_linkedin.py

It also writes linkedin.txt next to the code (gitignored) so you can open and
review it before pasting -- worth a skim, since LinkedIn PDF exports often
include your phone number and address.
"""

from pathlib import Path

from pypdf import PdfReader

HERE = Path(__file__).resolve().parent
PDF_PATH = HERE / "linkedin.pdf"
TXT_PATH = HERE / "linkedin.txt"


def extract_pdf_text(pdf_path: Path) -> str:
    """Pull the plain text out of a PDF, skipping pages that yield nothing."""
    reader = PdfReader(pdf_path)
    pages = (page.extract_text() for page in reader.pages)
    return "\n".join(text for text in pages if text).strip()


def main() -> None:
    if not PDF_PATH.is_file():
        raise SystemExit(f"No PDF found at {PDF_PATH}")

    text = extract_pdf_text(PDF_PATH)
    TXT_PATH.write_text(text, encoding="utf-8")

    print(text)
    print("-" * 60)
    print(f"Wrote {len(text):,} characters to {TXT_PATH}")
    print("Review it, then paste the contents into a Render secret file named 'linkedin.txt'.")


if __name__ == "__main__":
    main()
