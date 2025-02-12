<script setup>
import { onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

onMounted(() => {
    const token = route.query.access_token

    if (token) {
        localStorage.setItem("chronoJWTToken", token)
        router.push({ name: 'Profile Page' })
    } else {
        console.error('Токен не найден в URL')
        router.push({ name: 'Login' })
    }
})
</script>

<template>
    <div class="Lo">
        <p>Обработка авторизации...</p>
    </div>
</template>

<style>
@import "../../components/grey_style/LoginContainer.css";
</style>