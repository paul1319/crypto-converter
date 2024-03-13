from pydantic.dataclasses import dataclass

from app.dto.symbol import AddQuoteDTO


@dataclass
class Quote:
    symbol: str
    rate: float

    @classmethod
    def add(cls, dto: AddQuoteDTO) -> "Quote":
        return cls(symbol=dto.symbol, rate=dto.rate)
