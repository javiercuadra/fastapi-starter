from typing import List
from pydantic import BaseModel

class MathRequest(BaseModel):
    numbers: List[float] = []