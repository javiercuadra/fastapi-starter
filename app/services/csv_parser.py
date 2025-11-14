import csv
from io import StringIO
from typing import List, Dict

def parse_meds_csv(csv_text: str) -> List[Dict[str, str]]:
    """
    Takes raw CSV text and converts it into a list of dictionaries.
    Each dictionary corresponds to a medication entry.
    """

    # Convert raw text into a file-like object for csv.DictReader
    f = StringIO(csv_text)
    reader = csv.DictReader(f)

    # Convert to list of dicts
    rows = [dict(row) for row in reader]

    return rows