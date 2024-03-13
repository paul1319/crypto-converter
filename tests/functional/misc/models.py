from pydantic.dataclasses import dataclass


@dataclass
class QuoteModel:
    from_currency: str
    to_currency: str
    rate: float
