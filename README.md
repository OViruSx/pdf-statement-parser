# 📄 PDF Statement Parser

A Python tool for converting **Bank Muscat Savings** and **Bank Muscat Credit Card** PDF statements into clean, structured CSV files.

Supports:
- 🏦 Bank Muscat Savings Accounts  
- 💳 Bank Muscat Mastercard / Visa Credit Cards  
- 🔍 Automatic statement type detection  
- 📑 Multi-line description handling  
- 🚧 Non-tabular PDFs (texts only, no built-in tables)  
- 🖥 Optional Streamlit UI  

---

## 🚀 Features

### ✔ Automatic statement type detection  
Detects Savings vs Credit Card statements based on PDF content.

### ✔ Accurate table reconstruction  
Handles messy PDFs where rows visually align but aren’t actual tables.

### ✔ Multi-line descriptions  
Many credit card descriptions wrap across lines — this parser merges them correctly.

### ✔ Works across pages  
Parses tables cleanly even when they continue over multiple PDF pages.

### ✔ Output as UTF-8 CSV  
Easy to import into Excel, Sheets, or data pipelines.

---

## 📦 Installation

```bash
git clone https://github.com/OViruSx/pdf-statement-parser
cd pdf-statement-parser
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
🧠 Usage (CLI)
Basic:
bash
Copy code
python main.py statement.pdf
Specify output folder:
bash
Copy code
python main.py statement.pdf output_folder/
CSV file will appear in:

php-template
Copy code
output/<filename>_<detected_type>.csv
📂 Project Structure
pgsql
Copy code
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
🔍 Statement Type Detection
python
Copy code
def detect_statement_type(text: str):
    text = text.lower()

    if "value date" in text and "withdrawal" in text:
        return "bank_muscat_savings"

    if "transaction date" in text and "posting date" in text:
        return "bank_muscat_creditcard"

    return None
🏦 Savings Parser (Summary)
Handles columns:

Post Date

Value Date

Narration

Debit

Credit

Balance

Extracts words → groups into rows → assigns columns based on X-positions.

python
Copy code
with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        words = page.extract_words()
        # detect header, group rows, map columns...
💳 Credit Card Parser (Summary)
The hardest part — because statements look like this:

swift
Copy code
QAHA SPECIALITY COFFEE
14/11/2025 16/11/2025 MUSCAT OMR 2.100 -2.100
-
Parser handles both cases:

Case A — one-line rows
swift
Copy code
14/11/2025 16/11/2025 AL MEERA MUSCAT OMR 29.230 -29.230
Case B — description above dates
swift
Copy code
SHELL OMAN – AMRAT IND
11/11/2025 12/11/2025 AL AMRAT OMR 6.600 -6.600
🖥 Streamlit UI
Run:

bash
Copy code
streamlit run ui/streamlit_app.py
Allows:

Drag-and-drop PDF upload

Automatic parsing

CSV download

➕ Adding a New Bank Parser
1️⃣ Create a file:

bash
Copy code
parsers/my_new_bank.py
2️⃣ Implement:

python
Copy code
def parse_pdf(pdf_path, csv_path):
    ...
3️⃣ Register in main.py:

python
Copy code
PARSERS = {
    "bank_muscat_savings": bank_muscat_savings.parse_pdf,
    "bank_muscat_creditcard": bank_muscat_creditcard.parse_pdf,
    "my_new_bank": my_new_bank.parse_pdf
}
4️⃣ Add detection rules in detector.py.

⭐ Contributing
PRs and issue reports are welcome.

If this helped you, please star the repo ⭐
https://github.com/OViruSx/pdf-statement-parser

📜 License
MIT License.
