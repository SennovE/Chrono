from pydantic import BaseModel, Field


class CreateInvoiceRequest(BaseModel):
    shop_id: str = Field(..., description="Уникальный идентификатор магазина из личного кабинета")
    amount: int = Field(..., description="Сумма платежа в USD")
    currency: str = Field("USD", description="Валюта счета (например, USD)")