from app.database.models import DeadlineTask
from app.schemas import DeadlineGenerate, DeadlineTaskAICreare
from app.utils.user import User


from openai import OpenAI
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import exc
import datetime


async def generate_deadline(response: DeadlineGenerate, \
                        current_user: User, \
                        session: AsyncSession) -> bool:
    api_key = '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'
    client = OpenAI(api_key=api_key)

    completion = client.beta.chat.completions.parse(model="gpt-4o", messages=[
      {"role": "system", "content": f"Ты превращаешь текстовый запрос пользователя в одну моделей создания дедлайна. \
       Верни модель дедлайна по запросу пользователя. \
       Если пользователь не вводит точное время, выбери подходящее сам (например: рано вечером - в 18:00). Сейчас {datetime.datetime.now()}. \
        Не пиши никакое время в description, только описание события"},
      {"role": "user", "content": f'{response.text}'}],
      response_format=DeadlineTaskAICreare)
    
    ai_response = completion.choices[0].message.parsed
    date = datetime.datetime.strptime(ai_response.deadline_time, "%Y-%m-%dT%H:%M:%S")

    task = DeadlineTask(description=ai_response.description, deadline_time=date, \
                             author_id=current_user.id, author=current_user.username, status=0)

    session.add(task)
    try:
        await session.commit()
    except exc.IntegrityError:
        return False
    
    return True


