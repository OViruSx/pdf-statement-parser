import pdfplumber
import csv
import re

DATE_RE = re.compile(r"\d{2}/\d{2}/\d{4}")

HEADER = [
    "Transaction Date",
    "Posting Date",
    "Description",
    "Merchant City",
    "Currency",
    "Trans Amount",
    "Card Amount",
]


def parse_row(text: str):
    """
    Parse a single row string into:
    [tdate, pdate, description, city, currency, trans_amount, card_amount]

    Handles:
    - normal rows (date date desc city cur amt card)
    - description-first rows (QAHA, SHELL, HOME CENTRE, HYPERMAX, etc.)
    - payment rows ("Payment Received via Mobile", "Payment on cardholder")
    - non-OMR currency (e.g. USD) – kept as-is
    """
    # Flatten whitespace / newlines
    flat = " ".join(text.split()).split()
    if not flat:
        return None

    # ---- find dates ----
    date_indices = [i for i, tok in enumerate(flat) if DATE_RE.fullmatch(tok)]
    if len(date_indices) < 2:
        # no proper transaction pair → header / junk
        return None

    i1, i2 = date_indices[0], date_indices[1]
    tdate, pdate = flat[i1], flat[i2]

    # ---- find currency (OMR, USD, etc.) scanning from right ----
    cur_idx = None
    for i in range(len(flat) - 1, -1, -1):
        tok = flat[i]
        # 3-letter all-caps token after posting date → treat as currency
        if re.fullmatch(r"[A-Z]{3}", tok) and i > i2:
            cur_idx = i
            break

    if cur_idx is None or cur_idx + 2 >= len(flat):
        # can't confidently parse this row
        return None

    currency = flat[cur_idx]
    trans_amount = flat[cur_idx + 1]
    card_amount = flat[cur_idx + 2]

    # ---- special-case payment rows ----
    # e.g. "Payment Received via Mobile 24/10/2025 24/10/2025 OMR 515.208 515.208 Banking - Thank You"
    # or   "Payment on cardholder 24/10/2025 24/10/2025 OMR 69.125 69.125 account"
    if flat[0].lower() == "payment":
        before_desc = flat[0:i1]
        after_desc = flat[cur_idx + 3:]
        desc_tokens = before_desc + after_desc
        description = " ".join(desc_tokens).strip()
        city = ""  # no real merchant city for payments
        return [tdate, pdate, description, city, currency, trans_amount, card_amount]

    # ---- normal / description-first rows ----
    # City is *always* the token right before the currency (from your samples)
    city = flat[cur_idx - 1]

    # Two shapes:
    #   (A) date-first:   date date DESC ... CITY CUR AMT AMT
    #   (B) desc-first:   DESC ... date date CITY CUR AMT AMT
    if i1 == 0:
        # date-first row: description is between posting date and city
        # [ date, postdate, desc..., city, cur, amt, card ]
        desc_tokens = flat[i2 + 1: cur_idx - 1]
    else:
        # description-first row: description is everything before the first date
        # [ desc..., date, postdate, ..., city, cur, amt, card ]
        desc_tokens = flat[0:i1]

    description = " ".join(desc_tokens).strip()

    return [tdate, pdate, description, city, currency, trans_amount, card_amount]


def parse_pdf(pdf_path: str, csv_path: str):
    final_rows = [HEADER]

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:

            # Try strict table extraction first
            table = page.extract_table()

            # If no table found, try the more permissive version
            if not table:
                tables = page.extract_tables()
                if tables:
                    table = tables[0]

            # If still nothing, skip page
            if not table:
                continue

            # Process each extracted row
            for raw_row in table:
                if not raw_row:
                    continue

                # PDFPlumber returns a list of cells; your PDF puts everything in 1 cell
                cells = [c for c in raw_row if c]
                if not cells:
                    continue

                text = cells[0]
                parsed = parse_row(text)
                if parsed:
                    final_rows.append(parsed)

    # Save CSV
    with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerows(final_rows)

