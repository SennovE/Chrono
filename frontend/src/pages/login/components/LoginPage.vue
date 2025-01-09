<script setup>
import { ref, watch } from "vue"
import { registerUser, loginUser } from "./LoginFunctions.js"
import { useRouter } from "vue-router"

const router = useRouter()

const registration = ref(true)

const username = ref("")
const email = ref("")
const password = ref("")
const response = ref("")

async function registerUserWrap() {
    response.value = await registerUser(email.value, username.value, password.value)
    if (response.value === "") {
        await loginUserWrap()
    }
}

async function loginUserWrap() {
    response.value = await loginUser(username.value, password.value)
    if (response.value === "") {
        router.push({
            name: "Profile Page"
        })
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
        <div class="welcome-text">
            <h1>Добро пожаловать в <span class="chrono">Chrono!</span></h1>
            <h2>Зарегистрируйтесь или войдите в свой аккаунт</h2>
            <p class="error-msg" style="text-align: left;">{{ response }}</p>
        </div>

        <transition name="slide" mode="out-in">
            <div class="input-container" :key="registration">
                <input
                    :class="{ hidden: !registration }"
                    placeholder="Email"
                    v-model="email"
                />
                <input placeholder="Username" v-model="username"/>
                <input placeholder="Password" v-model="password" type="password" />

                <button v-if="registration" @click="registerUserWrap">Зарегистрироваться</button>
                <button v-else @click="loginUserWrap">Войти</button>

                <span
                    v-if="registration"
                    class="bottom-text"
                    @click="registration = !registration"
                >
                    Уже есть аккаунт (войти)
                </span>
                <span
                    v-else
                    class="bottom-text"
                    @click="registration = !registration"
                >
                    Еще нет аккаунта (зарегистрироваться)
                </span>
            </div>
        </transition>
    </div>
</template>

<style>
.left-text {
    text-align: left
}
</style>