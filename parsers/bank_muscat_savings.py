# parsers/bank_muscat_savings.py

import pdfplumber
import csv

# Column boundaries tuned from your debug:
# x0 ≈ 80, 160, 235, 585, 680, 799, etc.
COL_POSITIONS = [
    0,      # dummy / left margin
    120,    # Post Date
    200,    # Value Date
    570,    # Narration
    660,    # Debit
    760,    # Credit
    9999    # Balance (everything to the right)
]

FOOTER_KEYWORDS = [
    "case", "discrepancy", "receipt", "calling", "care@bankmuscat.com"
]

HEADER = ["Post Date", "Value Date", "Narration", "Debit", "Credit", "Balance"]


def _assign_columns(row):
    cols = [""] * 6
    for w in row:
        x = w["x0"]
        text = w["text"]
        for i in range(6):
            if COL_POSITIONS[i] <= x < COL_POSITIONS[i + 1]:
                cols[i] += text + " "
                break
    return [c.strip() for c in cols]


def _group_rows(words, tol=8):
    rows = []
    current = []
    last_y = None

    for w in words:
        y = w["top"]
        if last_y is None or abs(y - last_y) < tol:
            current.append(w)
        else:
            rows.append(current)
            current = [w]
        last_y = y

    if current:
        rows.append(current)

    return rows


def parse_pdf(pdf_path: str, csv_path: str):
    final_rows = []
    header_added = False

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            words = page.extract_words()

            # find header row by the word "Post"
            header_y = None
            for w in words:
                if w["text"].lower() == "post":
                    header_y = w["top"]
                    break
            if header_y is None:
                continue

            if not header_added:
                final_rows.append(HEADER)
                header_added = True

            # table words: below header
            table_words = [w for w in words if w["top"] > header_y + 5]

            grouped = _group_rows(table_words, tol=8)

            for row in grouped:
                if not row:
                    continue

                # remove footer rows – by Y & keywords
                min_y = min(w["top"] for w in row)
                if min_y > 1500:
                    continue
                if any(w["text"].lower() in FOOTER_KEYWORDS for w in row):
                    continue

                cols = _assign_columns(row)
                if not any(cols):
                    continue

                final_rows.append(cols)

    with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerows(final_rows)
