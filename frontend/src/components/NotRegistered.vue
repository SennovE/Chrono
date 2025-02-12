<script setup>
import { useRouter } from "vue-router"

const router = useRouter()
</script>

<template>
    <div class="not-registered">
        <div class="not-registered-content">
            <h1>Для использования надо зайти в аккаунт</h1>
            <button @click="router.push({ name: 'Registration' })">Зарегистрироваться</button>
            <button @click="router.push({ name: 'Login Page' })">Войти</button>
        </div>
    </div>
</template>


<style>
@import "./grey_style/NotRegistered.css";
</style>