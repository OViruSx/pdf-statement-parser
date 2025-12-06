🧾 PDF Statement Parser

A lightweight, extensible Python tool for parsing bank statements (Savings & Credit Card) into clean CSV files using pdfplumber.

This project is built to solve a common headache:
Bank statements come in messy PDF formats with multi-line descriptions, inconsistent spacing, and column shifts — especially for Bank Muscat savings and credit-card statements.

This parser cleans all of that into tidy, structured CSVs.
Fully offline. Fast. Extensible.

🚀 Features
✔️ Savings Account Parser

Extracts:

Post Date

Value Date

Narration

Withdrawals

Deposits

Balance

Handles:

Columns starting mid-page

Multi-line narration

Removing disclaimers / footers

✔️ Credit Card Parser

Extracts:

Transaction Date

Posting Date

Description

Merchant City

Currency

Transaction Amount

Card Amount

Handles:

Multi-line merchant names

Description lines appearing before the dates

Currency mismatches

International payments

No-table PDFs (text-only layout)

✔️ Auto-Detection

Feed the parser any PDF and it will automatically detect:

bank_muscat_savings
bank_muscat_creditcard


Additional parsers can be added easily.

✔️ CLI Tool

Run a statement through the parser:

python main.py sample.pdf


Output CSV is saved in output/.

📦 Project Structure
pdf-statement-parser/
│
├── main.py               # Entry point
├── detector.py           # Detect statement type
│
├── parsers/
│   ├── __init__.py
│   ├── bank_muscat_savings.py
│   └── bank_muscat_creditcard.py
│
├── ui/
│   └── streamlit_app.py  # (optional) small web UI
│
├── requirements.txt
└── README.md

🛠 Installation
git clone https://github.com/OViruSx/pdf-statement-parser
cd pdf-statement-parser
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

🔍 Usage
CLI Mode
python main.py path/to/statement.pdf


Optional output directory:

python main.py statement.pdf custom_output/

Streamlit UI (Optional)
streamlit run ui/streamlit_app.py


Upload any savings or credit-card PDF and get an instant CSV.

🧩 Adding Your Own Parsers

To support a new bank format:

Create a new file under parsers/

Implement a function:

def parse_pdf(pdf_path, csv_path):
    ...


Register it inside main.py:

PARSERS = {
    "bank_muscat_savings": bank_muscat_savings.parse_pdf,
    "bank_muscat_creditcard": bank_muscat_creditcard.parse_pdf,
    "new_bank_format": new_parser.parse_pdf
}


Add a detection rule in detector.py.

🧪 Supported PDFs (Examples)

You can test OCR/Extraction using:

Bank Muscat Savings Statements

Bank Muscat Credit Card Statements

More formats coming soon.

🧤 Limitations

Very messy scanned PDFs may require OCR first (Tesseract recommended).

Column detection assumes Bank Muscat’s standard formatting.

International statements may need custom rules.

🤝 Contributing

Pull requests are welcome!
Feel free to improve detection, add new banks, or enhance extraction logic.

📄 License

MIT License — free for personal & commercial use.

⭐ Like the project?

Give it a star on GitHub — it helps a lot!

👉 https://github.com/OViruSx/pdf-statement-parser
