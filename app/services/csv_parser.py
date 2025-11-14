import csv
from io import StringIO
from typing import List, Dict

def parse_meds_csv(csv_text: str, row_limit: int = 10000) -> List[Dict[str, str]]:
    """
    Takes raw CSV text and converts it into a list of dictionaries.
    Each dictionary corresponds to a medication entry.
    Raises ValueError if the CSV is empty, malformed, or exceeds row_limit.
    
    Args:
        csv_text: Raw CSV text to parse
        row_limit: Maximum number of rows to parse (default: 10000)
        
    Returns:
        List of dictionaries, each representing a medication entry
    """

    # Validate input
    if not csv_text or not csv_text.strip():
        raise ValueError("CSV text is empty.")

    # Convert raw text into a file-like object for csv.DictReader
    f = StringIO(csv_text)
    try:
        reader = csv.DictReader(f)
        rows = []
        for i, row in enumerate(reader):
            if i >= row_limit:
                raise ValueError(f"CSV row limit of {row_limit} exceeded.")
            rows.append(dict(row))
    except csv.Error as e:
        raise ValueError(f"Malformed CSV data: {e}")

    return rows