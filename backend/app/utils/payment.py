from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models.payment import Payment
from sqlalchemy.exc import IntegrityError
from app.utils.user import get_user_by_email




async def create_payment(session: AsyncSession, payment_id: str, email: str) -> bool:
    try:
        payment = Payment(id_user = payment_id,email = email)
        session.add(payment)
        await session.flush()
        await session.commit()
        return True
    except IntegrityError as ie:
        await session.rollback()
        return False
    except Exception as e:
        await session.rollback()

        raise HTTPException(status_code=500, detail=f"Ошибка при создании платежа {e}")


async def payment_success(session: AsyncSession, payment_id: str) -> bool:
    query = select(Payment).where(Payment.id_user == payment_id)
    result = await session.execute(query)
    payment_record = result.scalar_one_or_none()
    if not payment_record:
        return False

    user = await get_user_by_email(session, payment_record.email)
    if not user:
        return False

    user.premium = 1
    session.add(user)
    await session.commit() 
    return True