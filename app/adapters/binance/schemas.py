from app.utils.model import AppBaseModel


class BAQuote(AppBaseModel):
    symbol: str
    rate: float
