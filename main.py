# main.py
import sys
import os
import pdfplumber

from detector import detect_statement_type
from parsers import bank_muscat_savings, bank_muscat_creditcard

PARSERS = {
    "bank_muscat_savings": bank_muscat_savings.parse_pdf,
    "bank_muscat_creditcard": bank_muscat_creditcard.parse_pdf,
}

def main(pdf_path: str, out_dir: str = "output"):
    if not os.path.exists(pdf_path):
        print(f"[ERROR] File not found: {pdf_path}")
        return

    os.makedirs(out_dir, exist_ok=True)

    # Use first page text for detection
    with pdfplumber.open(pdf_path) as pdf:
        first_page = pdf.pages[0]
        words = first_page.extract_words()
        full_text = " ".join(w["text"].lower() for w in words)

    stype = detect_statement_type(full_text)

    if stype is None:
        print("[ERROR] Unknown statement type. Add a detector rule.")
        return

    print(f"[INFO] Detected statement type: {stype}")

    parser_func = PARSERS[stype]
    csv_path = os.path.join(
        out_dir,
        f"{os.path.splitext(os.path.basename(pdf_path))[0]}_{stype}.csv"
    )

    parser_func(pdf_path, csv_path)
    print(f"[OK] Parsed to: {csv_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <statement.pdf> [output_dir]")
    else:
        pdf_path = sys.argv[1]
        out_dir = sys.argv[2] if len(sys.argv) > 2 else "output"
        main(pdf_path, out_dir)
