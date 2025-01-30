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
@import "./Stiles.css";

.not-registered {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: #000000a5;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 9999;
    overflow: hidden;
}
.not-registered-content {
    width: 30%;
    background: linear-gradient(to left, var(--color-brighter-black), var(--color-black));
    padding: 1% 2% 1% 2%;
    border-radius: 8px;
    box-sizing: border-box;
    border: 1px solid var(--color-black);
    text-align: center;
}
</style>