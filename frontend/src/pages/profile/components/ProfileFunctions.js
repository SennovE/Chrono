

import axios from "axios"

export async function change_password(password) {
  if (!password) {
    return "Все поля должны быть заполнены"
  }
  try {
    await axios.post(
      `http://${import.meta.env.VITE_APP_BACKEND_URL}:8080/api/v1/settings/update_password`,
      { updated_password: password },
      {
        headers: {
          "Accept": "application/json",
          "Content-Type": "application/json",
        }
      }
    )
    return ""
  } catch (error) {
    return "Сетевая ошибка или сервер не ответил"
  }
}

export async function get_old_password() {
  try {
    const token = localStorage.getItem("token")
    if (!token) {
      return -1
    }
    const response = await axios.get(
      `http://${import.meta.env.VITE_APP_BACKEND_URL}:8080/api/v1/user/me`,
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    )
    return response.data.password
  } catch (error) {
    return -1
  }
}
