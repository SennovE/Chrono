from app.database.models import DeadlineTask, Schedule
from app.schemas import DeadlineGenerate, DeadlineTaskCreateForm, DeadlineTaskList, \
  ScheduleGenerate, ScheduleList, ScheduleUpdateForm
from app.utils.user import User


from openai import OpenAI
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import exc
import datetime
from pydantic import BaseModel
from fastapi import HTTPException
from typing import List

api_key = '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'

async def generate_deadline(response: DeadlineGenerate, \
                        current_user: User) -> list[DeadlineTask]:
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


async def schedule_generation(response: ScheduleGenerate, \
                              current_user: User) -> list[Schedule]:
   client = OpenAI(api_key=api_key)

   completion = client.beta.chat.completions.parse(model="gpt-4o", messages=[
      {"role": "system", "content": f"Ты генерируешь расписание (список задач с началом и концом выполнения) для пользователя по текстовому запросу. \
       Расписание должно быть составлено на целый день, составь его так, чтобы человек был максимально продуктивен и вовремя отдыхал, \
       Если ты считаешь, что в какой-то промежуток пользователю надо отдохнуть, не генерируй задач, которые занимают это время, просто оставь пустое место. \
       Если пользователь не вводит точное время, выбери подходящее сам (например: рано вечером - в 18:00). Сейчас {datetime.datetime.now()}. \
        Не пиши никакое время в name или text или указание дня недели, части дня, только описание события. Сначала идут предпочтения пользователя, то есть его личные настройки, \
        потом идет запрос - то, что пользователю. надо сделать в этот день. Учитывай предпочтения пользователя по дням недели, если пользователь пишет, \
        что обычно просыпается в 10, а по четвергам в 7, учитывай это и можешь ставить задачи раньше 10. start_time и end_time должны быть в формате %Y-%m-%dT%H:%M:%S"},
      {"role": "user", "content": f'Предпочтения пользователя: {current_user.text_settings}, запрос пользователя: {response.text}'}],
      response_format=ScheduleList)

   ai_response = completion.choices[0].message.parsed

   ans = []
   for task in ai_response.tasks:
     start_time = datetime.datetime.strptime(task.start_time, "%Y-%m-%dT%H:%M:%S")
     end_time = datetime.datetime.strptime(task.end_time, "%Y-%m-%dT%H:%M:%S")

     db_task = ScheduleUpdateForm(name=task.name, text=task.text, start_time=start_time, \
                                  end_time=end_time, recurring=task.recurring)

     ans.append(db_task)
  
   return ans