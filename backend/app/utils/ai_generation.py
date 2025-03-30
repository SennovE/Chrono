from app.database.models import DeadlineTask, Schedule
from app.schemas import DeadlineGenerate, DeadlineTaskCreateForm,\
  ScheduleGenerate, ScheduleUpdateForm, AddScheduleTasksAI
from app.utils.user import User, get_user_settings


from sqlalchemy.ext.asyncio import AsyncSession
import datetime
import aiohttp
import json


async def generate_deadline(response: DeadlineGenerate,
                            current_user: User,
                            session: AsyncSession,
                            api_key: str) -> list[DeadlineTask]:
    async def send_request() -> list[DeadlineTask]:
        url = "https://api.deepseek.com/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        settings = await get_user_settings(current_user, session)

        payload = {
            "model": "deepseek-chat",
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "Ты превращаешь текстовый запрос пользователя в одну или несколько моделей создания дедлайна. "
                        "Верни список дедлайнов по запросу пользователя. "
                        f"Если пользователь не вводит точное время, выбери подходящее сам (например: рано вечером - в 18:00). Сейчас {datetime.datetime.now()}. "
                        "Не пиши никакое время в description или указание дня недели, части дня, только описание события. Сначала идут предпочтения пользователя, то есть его личные настройки, "
                        "потом идет запрос - то, что ты должен добавить как дедлайн. Учитывай предпочтения пользователя по дням недели, если пользователь пишет, "
                        f"что обычно просыпается в 10, а по четвергам в 7, учитывай это и можешь ставить дедлайны раньше 10. deadline_time должен быть в формате %Y-%m-%dT%H:%M:%S."
                        "Верни json объекты { tasks: list[ { description: str, deadline_time: str } ] }"
                        )
                },
                {
                    "role": "user",
                    "content": f'Предпочтения пользователя: {settings.text_settings}, запрос пользователя: {response.text}'
                },
            ],
        }

        async with aiohttp.ClientSession() as client:
            async with client.post(url, json=payload, headers=headers) as resp:
                if resp.status == 200:
                    data = await resp.json()

                    ai_response_text = data["choices"][0]["message"]["content"]
                    if ai_response_text.startswith("```json"):
                        ai_response_text = ai_response_text[7:-3].strip()
                    ai_response = json.loads(ai_response_text)

                    ans = []
                    for task in ai_response["tasks"]:
                        date = datetime.datetime.strptime(task["deadline_time"], f"%Y-%m-%dT%H:%M:%S")
                        db_task = DeadlineTaskCreateForm(
                            description=task["description"],
                            deadline_time=date
                        )
                        ans.append(db_task)
                    return ans
                else:
                    return []
    
    ans = await send_request()
    return ans
    


async def schedule_generation(response: ScheduleGenerate, 
                              current_user: User, 
                              session: AsyncSession,
                              api_key: str) -> list[Schedule]:
    async def send_request() -> list[Schedule]:
        url = "https://api.deepseek.com/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        settings = await get_user_settings(current_user, session)

        payload = {
            "model": "deepseek-chat",
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "Ты генерируешь расписание (список задач с началом и концом выполнения) для пользователя по текстовому запросу. "
                        "Расписание должно быть составлено на целый день, составь его так, чтобы человек был максимально продуктивен и вовремя отдыхал, "
                        "Если ты считаешь, что в какой-то промежуток пользователю надо отдохнуть, не генерируй задач, которые занимают это время, просто оставь пустое место. "
                        f"Если пользователь не вводит точное время, выбери подходящее сам (например: рано вечером - в 18:00). Сейчас {datetime.datetime.now()}. "
                        "Не пиши никакое время в name или text или указание дня недели, части дня, только описание события. Сначала идут предпочтения пользователя, то есть его личные настройки, "
                        "потом идет запрос - то, что пользователю надо сделать в этот день. Учитывай предпочтения пользователя по дням недели, если пользователь пишет, "
                        f"что обычно просыпается в 10, а по четвергам в 7, учитывай это и можешь ставить задачи раньше 10. start_time и end_time должны быть в формате %Y-%m-%dT%H:%M:%S."
                        "Верни json объекты { tasks: list[ { name: str, text: str, start_time: str, end_time: str, recurring: bool } ] }"
                        )
                },
                {
                    "role": "user",
                    "content": f'Предпочтения пользователя: {settings.text_settings}, рабочее время пользователя: {settings.start_working} - {settings.end_working}, запрос пользователя: {response.text}'
                },
            ],
        }

        async with aiohttp.ClientSession() as client:
            async with client.post(url, json=payload, headers=headers) as resp:
                if resp.status == 200:
                    data = await resp.json()

                    ai_response_text = data["choices"][0]["message"]["content"]
                    if ai_response_text.startswith("```json"):
                        ai_response_text = ai_response_text[7:-3].strip()
                    ai_response = json.loads(ai_response_text)

                    ans = []
                    for task in ai_response["tasks"]:
                        start_time = datetime.datetime.strptime(task["start_time"], f"%Y-%m-%dT%H:%M:%S")
                        end_time = datetime.datetime.strptime(task["end_time"], f"%Y-%m-%dT%H:%M:%S")
                        db_task = ScheduleUpdateForm(
                            name=task["name"],
                            text=task["text"],
                            start_time=start_time,
                            end_time=end_time,
                            recurring=task["recurring"]
                        )
                        ans.append(db_task)
                    return ans
                else:
                    return []
    
    return await send_request()


async def add_schedule_tasks(response: AddScheduleTasksAI,
                             current_user: User,
                             session: AsyncSession,
                             api_key: str) -> list[Schedule]:
    async def send_request() -> list[Schedule]:
        url = "https://api.deepseek.com/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        settings = await get_user_settings(current_user, session)

        payload = {
            "model": "deepseek-chat",
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "Ты превращаешь текстовый запрос пользователя в одну или несколько моделей блока задачи в расписании. "
                        "Верни список блоков задач в расписании по запросу пользователя. "
                        f"Если пользователь не вводит точное время, выбери подходящее сам (например: рано вечером - в 18:00). Сейчас {datetime.datetime.now()}. "
                        "Не пиши никакое время в description или указание дня недели, части дня, только описание события. Сначала идут предпочтения пользователя, то есть его личные настройки, "
                        "потом идет запрос - то, что ты должен добавить как блоки задач в расписании. Учитывай предпочтения пользователя по дням недели, если пользователь пишет, "
                        f"что обычно просыпается в 10, а по четвергам в 7, учитывай это и можешь ставить дедлайны раньше 10. deadline_time должен быть в формате %Y-%m-%dT%H:%M:%S."
                        "Верни json объекты { tasks: list[ { name: str, text: str, start_time: str, end_time: str, recurring: bool } ] }"
                        )
                },
                {
                    "role": "user",
                    "content": f'Предпочтения пользователя: {settings.text_settings}, запрос пользователя: {response.text}'
                },
            ],
        }

        async with aiohttp.ClientSession() as client:
            async with client.post(url, json=payload, headers=headers) as resp:
                if resp.status == 200:
                    data = await resp.json()

                    ai_response_text = data["choices"][0]["message"]["content"]
                    if ai_response_text.startswith("```json"):
                        ai_response_text = ai_response_text[7:-3].strip()
                    ai_response = json.loads(ai_response_text)

                    ans = []
                    for task in ai_response["tasks"]:
                        start_time = datetime.datetime.strptime(task["start_time"], f"%Y-%m-%dT%H:%M:%S")
                        end_time = datetime.datetime.strptime(task["end_time"], f"%Y-%m-%dT%H:%M:%S")
                        db_task = ScheduleUpdateForm(
                            name=task["name"],
                            text=task["text"],
                            start_time=start_time,
                            end_time=end_time,
                            recurring=task["recurring"]
                        )
                        ans.append(db_task)
                    return ans
                else:
                    return []
    
    ans = await send_request()
    return ans