# detector.py

def detect_statement_type(text: str) -> str | None:
    """
    Simple rule-based statement type detector.
    Add more rules as needed.
    """

    t = text.lower()

    if "account type" in t and "post date" in t and "narration" in t:
        return "bank_muscat_savings"

    if "transactions list" in t and "description of transaction" in t:
        return "bank_muscat_creditcard"

    return None
