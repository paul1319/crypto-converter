from pydantic import Field

from app.utils.model import AppBaseModel


class ConvertResponse(AppBaseModel):
    amount: float = Field(description="Converted amount")
    rate: float = Field(description="Conversion rate")
