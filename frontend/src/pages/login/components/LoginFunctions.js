import axios from "axios"


export async function registerUser(email, username, password) {
    try {
        await axios.post("http://localhost:8080/api/v1/user/register", {
            email: email,
            username: username,
            password: password
        }, {
            headers: {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
        })
        return "Успешная регистрация"
    } catch (error) {
        if (error.response) {          
            if (error.response.status === 400) {
                return "Почта или имя пользователя уже занято"
            } else if (error.response.status === 422) {
                return error.response.data.detail[0].ctx.reason
            }
        } else {
            return "Сетевая ошибка или сервер не ответил"
        }
    }
}

export async function loginUser(username, password) {
    try {
        const res = await axios.post("http://localhost:8080/api/v1/user/token", {
            username: username,
            password: password
        }, {
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            }
        })
        const token = res.data.access_token
        localStorage.setItem('chronoJWTToken', token)
        return "Успешный вход"
    } catch (error) {
        if (error.response) {          
            if (error.response.status === 401) {
                return "Введен невеный пароль или имя"
            }
        } else {
            return "Сетевая ошибка или сервер не ответил"
        }
    }
}