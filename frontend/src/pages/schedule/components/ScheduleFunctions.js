import axios from "axios";

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

function getToken(router) {
    const token = localStorage.getItem("chronoJWTToken")
    if (!token) {
        redirectToLogin(router)
    }
    return token
}

export async function authUser(router) {
    try {
        const token = getToken(router);
        const response = await axios.get("http://localhost:8080/api/v1/user/me", {
            headers: {
                "Authorization": `Bearer ${token}`,
            },
        })
        return response.data
    } catch (error) {
        redirectToLogin(router)
    }
}

export async function addScheduleTask(router, name, descriptionText, startDate, endDate, recurring) {
    if (name === "" ||
        descriptionText === "" ||
        startDate === "" ||
        endDate === "" ||
        recurring === ""
    ) {
        return "Все поля должны быть заполнены"
    } else if (startDate > endDate) {
        return "Время начала должно быть меньше конца"
    }
    try {
        const token = getToken(router);
        await axios.post("http://localhost:8080/api/v1/schedule/", {
            name: name,
            text: descriptionText,
            start_time: startDate,
            end_time: endDate,
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