import axios from "axios";

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

export async function addScheduleTask(router, descriptionText, startDate, endDate, recurring) {
    if (descriptionText === "" || startDate === "" || endDate === "" || recurring === "") {
        return "Все поля должны быть заполнены"
    }
    try {
        const token = getToken(router);
        await axios.post("http://localhost:8080/api/v1/schedule/", {
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