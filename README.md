📄 PDF Statement Parser

A Python tool for extracting structured data from Bank Muscat Savings and Bank Muscat Credit Card PDF statements and exporting them into clean CSV files.

It handles:

multi-line descriptions

badly aligned text

inconsistent x/y layouts

no-table PDFs (pure text only)

auto-detection of statement type

All using pdfplumber.

📦 Installation
git clone https://github.com/OViruSx/pdf-statement-parser
cd pdf-statement-parser
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

🚀 Usage
CLI mode
python main.py path/to/statement.pdf


Output CSV will be saved in:

output/<filename>_<type>.csv

Specify output folder
python main.py statement.pdf my_output/

🧠 Project Structure
pdf-statement-parser/
│
├── main.py
├── detector.py
│
├── parsers/
│   ├── bank_muscat_savings.py
│   ├── bank_muscat_creditcard.py
│   └── __init__.py
│
├── ui/
│   └── streamlit_app.py
│
├── requirements.txt
└── README.md

🔍 Auto-Detection Logic (detector.py)
def detect_statement_type(text: str):
    text = text.lower()

    if "value date" in text and "withdrawal" in text:
        return "bank_muscat_savings"

    if "transaction date" in text and "posting date" in text:
        return "bank_muscat_creditcard"

    return None

🧾 Savings Parser (Excerpt)
import pdfplumber
import csv

def parse_pdf(pdf_path, csv_path):
    rows = []
    headers = ["Post Date", "Value Date", "Narration", "Withdrawal", "Deposit", "Balance"]

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            words = page.extract_words()

            # detect table start → find "Post Date"
            header_y = None
            for w in words:
                if w["text"].lower() == "post":
                    header_y = w["top"]
                    break

            if header_y is None:
                continue

            table_words = [w for w in words if w["top"] > header_y]

            # group row by y
            groups = group_rows(table_words)

            for g in groups:
                cols = assign_columns(g)
                rows.append(cols)

    with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

💳 Credit Card Parser (Excerpt)

Handles:

multi-line descriptions

description appearing before dates

foreign currency transactions

rows like:

QAHA SPECIALITY COFFEE
14/11/2025 16/11/2025 MUSCAT OMR 2.100 -2.100
-

Parsing logic
def parse_row(text):
    lines = text.strip().split("\n")

    # Case 1: description ABOVE the dates
    if len(lines) == 3 and re.match(DATE_PAIR, lines[1]):
        desc = lines[0].strip()
        parts = lines[1].split()
        txn = parts[0]
        post = parts[1]
        city = parts[-4]
        curr = parts[-3]
        amt1 = parts[-2]
        amt2 = parts[-1]
        return [txn, post, desc, city, curr, amt1, amt2]

    # Case 2: normal one-line row
    parts = text.split()
    if re.match(DATE_PAIR, f"{parts[0]} {parts[1]}"):
        txn = parts[0]
        post = parts[1]
        rest = parts[2:-4]
        desc = " ".join(rest)
        city = parts[-4]
        curr = parts[-3]
        amt1 = parts[-2]
        amt2 = parts[-1]
        return [txn, post, desc, city, curr, amt1, amt2]

    return None

🖥 Streamlit UI

Run it with:

streamlit run ui/streamlit_app.py


Features:

drag & drop PDFs

automatic statement-type detection

CSV download button

➕ Adding a New Bank Format

Create a parser:

parsers/my_new_bank.py


Implement:

def parse_pdf(pdf_path, csv_path):
    ...


Register it:

PARSERS = {
    "bank_muscat_savings": bank_muscat_savings.parse_pdf,
    "bank_muscat_creditcard": bank_muscat_creditcard.parse_pdf,
    "my_new_bank": my_new_bank.parse_pdf
}


Add detection logic in detector.py

That's it.

⚠️ Limitations

Very dirty scanned PDFs may require OCR (Tesseract recommended).

Format changes by the bank can break parsing (but easy to adjust).

Multi-currency rows may require extra handling.

📄 License

MIT License.

⭐ Support

If you like the project, give it a star on GitHub:

👉 https://github.com/OViruSx/pdf-statement-parser
