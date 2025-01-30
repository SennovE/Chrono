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

export async function addScheduleTask(router, name, descriptionText, startDate, startTime, endTime, recurring) {
    if (name === "" ||
        startTime === "" ||
        endTime === "" ||
        recurring === ""
    ) {
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
            recurring: recurring
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

export function makeWeekDates() {
    const currentDate = new Date()
    const dayOfWeek = currentDate.getDay()
    const distanceToMonday = dayOfWeek === 0 ? -6 : 1 - dayOfWeek
    const monday = new Date(currentDate)
    monday.setDate(currentDate.getDate() + distanceToMonday)
    monday.setHours(0, 0, 0, 0)
    const weekDates = []
    for (let i = 0; i < 7; i++) {
        const weekDay = new Date(monday)
        weekDay.setDate(monday.getDate() + i)
        weekDates.push(weekDay.getDate())
    }
    return weekDates
}

export function makeTime(ampm) {
    let times = [""]
    if (ampm.value) {
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
