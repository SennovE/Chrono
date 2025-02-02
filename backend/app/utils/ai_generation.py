from app.database.models import DeadlineTask
from app.schemas import DeadlineGenerate, DeadlineTaskAICreare, DeadlineTaskCreateForm
from app.utils.user import User


from openai import OpenAI
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import exc
import datetime
from pydantic import BaseModel
from fastapi import HTTPException

class DeadlineTaskList(BaseModel):
  tasks: list[DeadlineTaskAICreare]

  class Config:
        arbitrary_types_allowed = True


async def generate_deadline(response: DeadlineGenerate, \
                        current_user: User) -> list[DeadlineTask]:
    api_key = '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'
    client = OpenAI(api_key=api_key)

    completion = client.beta.chat.completions.parse(model="gpt-4o", messages=[
      {"role": "system", "content": f"Ты превращаешь текстовый запрос пользователя в одну или несколько моделей создания дедлайна. \
       Верни список дедлайнов по запросу пользователя. \
       Если пользователь не вводит точное время, выбери подходящее сам (например: рано вечером - в 18:00). Сейчас {datetime.datetime.now()}. \
        Не пиши никакое время в description или указание дня недели, части дня, только описание события. Сначала идут предпочтения пользователя, то есть его личные настройки, \
        потом идет запрос - то, что ты должен добавить как дедлайн. Учитывай предпочтения пользователя по дням недели, если пользователь пишет, \
        что обычно просыпается в 10, а по четвергам в 7, учитывай это и можешь ставить дедлайны раньше 10."},
      {"role": "user", "content": f'Предпочтения пользователя: {current_user.text_settings}, запрос пользователя: {response.text}'}],
      response_format=DeadlineTaskList)
    
    ai_response = completion.choices[0].message.parsed

    ans = []
    for task in ai_response.tasks:
      date = datetime.datetime.strptime(task.deadline_time, "%Y-%m-%dT%H:%M:%S")

      db_task = DeadlineTaskCreateForm(description=task.description, deadline_time=date)

      ans.append(db_task)
    
    return ans


async def submit_ai_gen(tasks: list[DeadlineTaskCreateForm], \
                        current_user: User, \
                        session: AsyncSession) -> bool:
    for task in tasks:
        task_data = task.model_dump()
        task_data["author_id"] = current_user.id
        task_data["author"] = current_user.username
        task_data["status"] = 0
        db_task = DeadlineTask(**task_data)

        session.add(db_task)
    
    try:
        session.commit()
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    
    return True
