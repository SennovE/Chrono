
from fastapi import HTTPException
import httpx
from typing import Dict
from pydantic import BaseModel, Field

class CreateInvoiceRequest(BaseModel):
    shop_id: str = Field(..., description="Уникальный идентификатор магазина из личного кабинета")
    amount: float = Field(..., description="Сумма платежа в USD")
    currency: str = Field("USD", description="Валюта счета (например, USD)")

class PaymentAPI:
    def __init__(self, api_key: str, base_url: str = "https://api.cryptocloud.plus/v1"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Token {self.api_key}",
            "Content-Type": "application/json"
        }

    async def create_invoice(self, data: CreateInvoiceRequest, locale: str = "ru") -> Dict:
        url = f"{self.base_url}/invoice/create"
        params = {"locale": locale}
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=self.headers, params=params, json=data.dict())
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(status_code=response.status_code, detail=response.text)
    async def test(self):
        url = f"{self.base_url}/invoice/create"
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=self.headers)
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(status_code=response.status_code, detail=response.text)
