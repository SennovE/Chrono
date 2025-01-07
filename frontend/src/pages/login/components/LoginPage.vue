<script setup>
import { ref, watch } from "vue"
import axios from "axios"

const registration = ref(true)

const username = ref("")
const email = ref("")
const password = ref("")
const response = ref("")

async function registerUser() {
    try {
        await axios.post("http://localhost:8080/api/v1/user/register", {
            email: email.value,
            username: username.value,
            password: password.value
        }, {
            headers: {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
        })
        response.value = "Успешная регистрация"
    } catch (error) {
        if (error.response) {          
            if (error.response.status === 400) {
                response.value = "Почта или имя пользователя уже занято"
            } else if (error.response.status === 422) {
                response.value = error.response.data.detail[0].ctx.reason
            }
        } else {
            response.value = "Сетевая ошибка или сервер не ответил"
        }
    }
}

async function loginUser() {
    try {
        const res = await axios.post("http://localhost:8080/api/v1/user/token", {
            username: username.value,
            password: password.value
        }, {
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            }
        })
        const token = res.data.access_token
        localStorage.setItem('chronoJWTToken', token)
        response.value = "Успешный вход"
    } catch (error) {
        if (error.response) {          
            if (error.response.status === 401) {
                response.value = "Введен невеный пароль или имя"
            }
        } else {
            response.value = "Сетевая ошибка или сервер не ответил"
        }
    }
}

function clearFields() {
    username.value = ""
    email.value = ""
    password.value = ""
    response.value = ""
}

watch(registration, clearFields)
</script>

<template>
    <div class="container">
        <div class="welcomeText">
            <h1>Добро пожаловать в <span class="chrono">Chrono!</span></h1>
            <h2>Зарегистрируйтесь или войдите в свой аккаунт</h2>
            <p>{{ response }}</p>
        </div>
      
        <transition name="slide" mode="out-in">
            <div class="inputContainer" :key="registration">
                <input
                    :class="{ hidden: !registration }"
                    placeholder="Email"
                    v-model="email"
                />
                <input placeholder="Username" v-model="username"/>
                <input placeholder="Password" v-model="password" type="password" />
          
                <button v-if="registration" @click="registerUser">Зарегистрироваться</button>
                <button v-else @click="loginUser">Войти</button>
          
                <span
                    v-if="registration"
                    class="bottomText"
                    @click="registration = !registration"
                >
                    Уже есть аккаунт (войти)
                </span>
                <span
                    v-else
                    class="bottomText"
                    @click="registration = !registration"
                >
                    Еще нет аккаунта (зарегистрироваться)
                </span>
            </div>
        </transition>
    </div>
</template>

<style>
    @import "./LoginStile.css";
</style>