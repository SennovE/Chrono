import axios from "axios";

export async function authUser() {
    try {
        const token = getToken();
        if (token == null) {
            return -1
        }
        const response = await axios.get(`http://${process.env.VUE_APP_BACKEND_URL}:8080/api/v1/user/me`, {
            headers: {
                "Authorization": `Bearer ${token}`,
            },
        })
        return response.data
    } catch (error) {
        return -1
    }
}

export async function deleteTask(router, taskId) {
    try {
        const token = getToken();
        if (token == null) {
            redirectToLogin(router)
            return
        }
        await axios.delete(`http://${process.env.VUE_APP_BACKEND_URL}:8080/api/v1/schedule/`, {
            data: taskId,
            headers: {
                "Accept": "application/json",
                "Authorization": `Bearer ${token}`,
                "Content-Type": "application/json",
            },
        })
        return
    } catch (error) {
        return
    }
}

export async function updateTask(router, taskId, name, descriptionText, startDate,
                                 startTime, endTime, recurring, group_id) {
    try {
        const token = getToken();
        if (token == null) {
            redirectToLogin(router)
            return -1
        }
        await axios.put(`http://${process.env.VUE_APP_BACKEND_URL}:8080/api/v1/schedule/`, {
            task_id: taskId,
            updated_task: {
                name: name,
                text: descriptionText,
                start_time: `${startDate}T${startTime}`,
                end_time: `${startDate}T${endTime}`,
                recurring: recurring,
                group_id: group_id ? group_id : "00000000-0000-0000-0000-000000000000",
            }
        }, {
            headers: {
                "Accept": "application/json",
                "Authorization": `Bearer ${token}`,
                "Content-Type": "application/json",
            },
        })
        return ""
    } catch (error) {
        if (error.response.data.detail[0].msg === "start_time should be less than end_time") {
            return "Время начала должно быть меньше конца"
        } else if (error.response.data.detail[0].msg.includes("datetime")) {
            return "Дата должна быть реальной"
        }
        return error.response.data.detail[0].msg
    }
}

export async function addScheduleTask(router, name, descriptionText, startDate,
                                      startTime, endTime, recurring, group_id) {
    if (name === "" || startTime === "" || endTime === "" || recurring === "") {
        return "Не все обязательные поля заполнены"
    } else if (startTime > endTime) {
        return "Время начала должно быть меньше конца"
    }
    try {
        const token = getToken();
        if (token == null) {
            redirectToLogin(router)
            return -1
        }
        await axios.post(`http://${process.env.VUE_APP_BACKEND_URL}:8080/api/v1/schedule/`, {
            name: name,
            text: descriptionText,
            start_time: `${startDate}T${startTime}`,
            end_time: `${startDate}T${endTime}`,
            recurring: recurring,
            group_id: group_id ? group_id : null,
        }, {
            headers: {
                "Accept": "application/json",
                "Authorization": `Bearer ${token}`,
                "Content-Type": "application/json",
            },
        })
        return ""
    } catch (error) {
        if (error.response.data.detail[0].msg === "start_time should be less than end_time") {
            return "Время начала должно быть меньше конца"
        } else if (error.response.data.detail[0].msg.includes("datetime")) {
            return "Дата должна быть реальной"
        }
        return error.response.data.detail[0].msg
    }
}

export async function getScheduleTasks(router) {
    try {
        const token = getToken();
        if (token == null) {
            redirectToLogin(router)
            return -1
        }
        const response = await axios.get(`http://${process.env.VUE_APP_BACKEND_URL}:8080/api/v1/schedule/`, {
            headers: {
                "Accept": "application/json",
                "Authorization": `Bearer ${token}`,
            },
        })
        return response.data
    } catch (error) {
        return {
            "0": [],
            "1": [],
            "2": [],
            "3": [],
            "4": [],
            "5": [],
            "6": [],
        }
    }
}

export async function getTasksGroups(router) {
    try {
        const token = getToken();
        if (token == null) {
            redirectToLogin(router)
            return -1
        }
        const response = await axios.get(`http://${process.env.VUE_APP_BACKEND_URL}:8080/api/v1/task_groups/all/`, {
            headers: {
                "Accept": "application/json",
                "Authorization": `Bearer ${token}`,
            },
        })
        return response.data
    } catch (error) {
        return []
    }
}

export async function deleteTasksGroup(router, groupId) {
    try {
        const token = getToken();
        if (token == null) {
            redirectToLogin(router)
            return
        }
        await axios.delete(`http://${process.env.VUE_APP_BACKEND_URL}:8080/api/v1/task_groups/`, {
            data: groupId,
            headers: {
                "Accept": "application/json",
                "Authorization": `Bearer ${token}`,
                "Content-Type": "application/json",
            },
        })
        return
    } catch (error) {
        return
    }
}

export async function addTasksGroup(router, name, color) {
    if (name === "" || color === "") {
        return "Не все обязательные поля заполнены"
    }
    const regex = /^#[0-9A-Fa-f]{6}$/;
    if (!regex.test(color)) {
        return "Цвет должен быть в формате '0f0f0f'"
    }
    try {
        const token = getToken();
        if (token == null) {
            redirectToLogin(router)
            return -1
        }
        await axios.post(`http://${process.env.VUE_APP_BACKEND_URL}:8080/api/v1/task_groups/`, {
            name: name,
            color: color,
        }, {
            headers: {
                "Accept": "application/json",
                "Authorization": `Bearer ${token}`,
                "Content-Type": "application/json",
            },
        })
        return ""
    } catch (error) {
        return error.response.data.detail[0].msg
    }
}

export async function updateTasksGroup(router, groupId, name, color) {
    if (name === "" || color === "") {
        return "Не все обязательные поля заполнены"
    }
    const regex = /^#[0-9A-Fa-f]{6}$/;
    if (!regex.test(color)) {
        return "Цвет должен быть в формате '0f0f0f'"
    }
    try {
        const token = getToken();
        if (token == null) {
            redirectToLogin(router)
            return -1
        }
        await axios.put(`http://${process.env.VUE_APP_BACKEND_URL}:8080/api/v1/task_groups/`, {
            id: groupId,
            name: name,
            color: color,
        }, {
            headers: {
                "Accept": "application/json",
                "Authorization": `Bearer ${token}`,
                "Content-Type": "application/json",
            },
        })
        return ""
    } catch (error) {
        return error.response.data.detail[0].msg
    }
}

export async function addTasksGroupByCode(router, code) {
    if (code === "") {
        return "Не все обязательные поля заполнены"
    }
    try {
        const token = getToken();
        if (token == null) {
            redirectToLogin(router)
            return -1
        }
        await axios.post(
            `http://${process.env.VUE_APP_BACKEND_URL}:8080/api/v1/task_groups/add_by_code`,
            code,
            {
                headers: {
                    "Accept": "application/json",
                    "Authorization": `Bearer ${token}`,
                    "Content-Type": "application/json",
                }
            }
        )
        return ""
    } catch (error) {
        return error.response.data.detail[0].msg
    }
}

export function makeWeekDates(currentDate, daysNumber) {
    const dayOfWeek = currentDate.getDay()
    let firstDay = null
    if (daysNumber == 7) {
        const distanceToMonday = dayOfWeek === 0 ? -6 : 1 - dayOfWeek
        firstDay = new Date(currentDate.getTime() + distanceToMonday * 24 * 60 * 60 * 1000)
    } else {
        firstDay = new Date(currentDate.getTime())
    }
    firstDay.setHours(0, 0, 0, 0)
    const weekDates = []
    for (let i = 0; i < daysNumber; i++) {
        const weekDay = new Date(firstDay.getTime() + i * 24 * 60 * 60 * 1000);
        weekDates.push(weekDay)
    }
    return weekDates
}

export function makeTime(am_pm) {
    let times = ["0:00"]
    if (am_pm.value) {
        for (let i = 1; i < 12 + 1; ++i) {
            times.push(`${i}:00 am`)
        }
        for (let i = 1; i < 12; ++i) {
            times.push(`${i}:00 pm`)
        }
    } else {
        for (let i = 1; i < 24; ++i) {
            times.push(`${i}:00`)
        }
    }
    return times
}

export function getMonthName(num) {
    const months = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]
    return months[num]
}

function redirectToLogin(router) {
    router.push({
        name: "Login Page",
    })
}

function getToken() {
    const token = localStorage.getItem("chronoJWTToken")
    if (!token) {
        return null
    }
    return token
}

export function currentTimeFilter(task, time, date) {
    if (`${task.start_hours}:00` != time) {
        return false
    }
    if (task.recurring) {
        return true
    }
    const year = date.getFullYear()
    const month = String(date.getMonth() + 1).padStart(2, '0')
    const day = String(date.getDate()).padStart(2, '0')
    if (task.year == year && task.month == month && task.day == day) {
        return true
    }
    return false
}

export async function AIGenerationFullDay(userText, startDate) {
    if (userText == "") {
        return "Введите запрос"
    }
    try {
        const token = getToken();
        const response = await axios.post(
            `http://${process.env.VUE_APP_BACKEND_URL}:8080/api/v1/schedule/schedule_generation`,
            { text: userText + '\n Расписание должно быть на дату: ' + startDate },
            {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            }
        );
        return response.data;
    } catch (error) {
        return "Error AI generation" + error;
    }
}

export async function AIGeneration(userText, startDate) {
    if (userText == "") {
        return "Введите запрос"
    }
    try {
        const token = getToken();
        const response = await axios.post(
            `http://${process.env.VUE_APP_BACKEND_URL}:8080/api/v1/schedule/add_schedule_tasks_ai`,
            { text: userText + '\n Расписание должно быть на дату: ' + startDate },
            {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            }
        );
        return response.data;
    } catch (error) {
        return "Error AI generation" + error;
    }
}


export async function SendAISchedule(aiSchedule) {
    try {
        const token = getToken();
        const tasksPayload = aiSchedule.map(task => ({
            name: task.name,
            text: task.text,
            start_time: new Date(task.start_time).toISOString(),
            end_time: new Date(task.end_time).toISOString(),
            recurring: task.recurring
        }));

        await axios.post(
            `http://${process.env.VUE_APP_BACKEND_URL}:8080/api/v1/schedule/send_ai_schedule`,
            tasksPayload,
            {
                headers: {
                    Authorization: `Bearer ${token}`,
                    "Content-Type": "application/json",
                },
            }
            );
      } catch (error) {
            console.error("Error submitting AI tasks:", error);
    }
}
