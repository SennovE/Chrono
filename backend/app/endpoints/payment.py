from fastapi import APIRouter, Form,Security, HTTPException, Depends, status
from app.config import get_settings, DefaultSettings 
from app.utils.payment import  create_payment, payment_success
from app.utils.payment_manager import  PaymentAPI
from typing import Annotated
from app.utils.user import get_current_user
from app.database.connection import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.payment import CreateInvoiceRequest
from app.database.models.payment import Payment

def get_payment_api(settings: DefaultSettings = Depends(get_settings)) -> PaymentAPI:
    return settings.pay_client

api_router = APIRouter(
    prefix="/payment",
    tags=["Payment"]
)

@api_router.post("/invoice/create", status_code=status.HTTP_200_OK)
async def create_invoice_endpoint(
    invoice: CreateInvoiceRequest,
    locale: str = "ru",
    payment_api = Depends(get_payment_api),
    user = Security(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    try:
        result = await payment_api.create_invoice(invoice, locale)

        payment_result = await create_payment(session, result['invoice_id'],user.email)
        if (payment_result):
            return result
        else:
            raise HTTPException(status_code=500, detail="Платеж не создан")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.post("/postback", status_code=200)
async def handle_postback(
    status: str = Form(...),
    invoice_id: str = Form(...),
    amount_crypto: str = Form(...),
    currency: str = Form(...),
    order_id: str = Form(...),
    token: str = Form(...),
    session: AsyncSession = Depends(get_session)
):
    if (status == "success"):
        result = await payment_success(session, invoice_id)
        if (result):
            return "Подписка активна"
        else:
            raise HTTPException(status_code=500, detail='хз')
    else:
        raise HTTPException(status_code=500, detail="Платеж не выполнен")
