from dataclasses import dataclass


@dataclass
class AddQuoteDTO:
    symbol: str
    rate: float
