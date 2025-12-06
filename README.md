📄 PDF Statement Parser

A powerful Python tool that converts Bank Muscat Savings and Bank Muscat Credit Card PDF statements into clean, structured CSV files — even when the PDFs contain multi-line descriptions, wrapped merchant names, misaligned columns, or inconsistent formatting.

This project uses pdfplumber (not OCR) and applies smart parsing logic to extract reliable financial data.

🚀 Features

🔍 Automatic statement type detection

📑 Parses:

- Bank Muscat Savings statements

- Bank Muscat Credit Card statements

🧠 Handles difficult layouts:

- Multi-line descriptions

- Merchant names spanning lines
 
- Broken table rows

- 📄 Multi-page PDF support

- 📊 Clean CSV output

- 🛠 Extensible architecture (easily add new banks)

📦 Installation
```
git clone https://github.com/OViruSx/pdf-statement-parser.git
cd pdf-statement-parser

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```
▶️ Usage

Parse any statement:

python main.py path/to/statement.pdf


CSV output will be saved to:
```
output/<filename>_<type>.csv
```

You can specify a custom output directory:

python main.py statement.pdf my_output_folder

🧠 How It Works
1️⃣ Statement Type Detection

detector.py extracts text from the first page and checks for known patterns:
```python
def detect_statement_type(text):
    if "post date" in text and "debit" in text:
        return "bank_muscat_savings"

    if "transaction posting" in text:
        return "bank_muscat_creditcard"

    return None
```
2️⃣ Savings Statement Parsing

bank_muscat_savings.py extracts columns like:
```
Post Date | Value Date | Narration | Debit | Credit | Balance
```

It uses text coordinates from pdfplumber to align data properly.

3️⃣ Credit Card Statement Parsing

bank_muscat_creditcard.py handles complex, multi-line rows such as:
```
QAHA SPECIALITY COFFEE
14/11/2025 16/11/2025 MUSCAT OMR 2.100 -2.100
-
```

Which becomes:
```
14/11/2025,16/11/2025,QAHA SPECIALITY COFFEE,MUSCAT,OMR,2.100,-2.100
```

The parser:

Detects the header row by coordinates

Groups rows using Y-axis clustering

Fixes wrapped merchant names

Separates city, dates, and amounts

Cleans broken lines and stray characters

📂 Project Structure
pdf-statement-parser/
│
├── main.py
├── detector.py
├── README.md
├── requirements.txt
│
├── parsers/
│   ├── bank_muscat_savings.py
│   └── bank_muscat_creditcard.py
│
└── ui/
    └── streamlit_app.py

🖥️ Optional GUI (Streamlit)

Run the web UI:
```pyhton
streamlit run ui/streamlit_app.py
```

Upload a PDF → automatically get the parsed CSV.

📊 Example Output (Credit Card)
```
Transaction Date,Posting Date,Description,Merchant City,Currency,Trans Amount,Card Amount
15/11/2025,16/11/2025,BAHARALKARAM,OM,OMR,2.600,-2.600
14/11/2025,16/11/2025,AL MEERA MARKETS,MUSCAT,OMR,29.230,-29.230
14/11/2025,16/11/2025,QAHA SPECIALITY COFFEE,MUSCAT,OMR,2.100,-2.100
```
🛠 Extending the Project

Add a new parser:

Create:
```
parsers/bank_xyz.py
```

Add your parse function:
```python
def parse_pdf(pdf_path, csv_path):
    ...
```

Register it in main.py:
```pyhton
PARSERS = {
    "bank_muscat_savings": bank_muscat_savings.parse_pdf,
    "bank_muscat_creditcard": bank_muscat_creditcard.parse_pdf,
    "bank_xyz": bank_xyz.parse_pdf,
}
```
🤝 Contributing

Pull requests are welcome.

If you’d like to add a new bank parser, open an issue and attach a sanitized sample PDF so the layout can be mapped correctly.

📜 License

MIT License — do whatever you want with it.
