<script setup>
import { useRouter } from "vue-router";

const router = useRouter();
</script>

<template>
    <div class="top-nav">
        <ul>
            <li @click="router.push({name: 'Welcome'})"><b>Главная</b></li>
            <li @click="router.push({name: 'Schedule Page'})"><b>Расписание</b></li>
            <li @click="router.push({name: 'Deadlines Page'})"><b>Дедлайны</b></li>
            <li
                class="right-button"
                @click="router.push({name: 'Profile Page'})"
            ><b>Профиль</b></li>
        </ul>
    </div>
</template>

<style>
.top-nav {
    width: 100%;
    background: linear-gradient(to left, var(--color-brighter-black), var(--color-black));
    position: fixed;
    top: 0;
    left: 0;
    box-shadow: 
        0px 0px 5px white,
        0px 0px 10px var(--color-deep-purple),
        0px 0px 20px var(--color-deep-purple),
        0px 0px 50px var(--color-deep-purple);
    z-index: 999;
}

.top-nav ul {
    display: flex;
    list-style-type: none;
    justify-content: flex-start;
}

.top-nav li {
    display: block;
    padding: 15px 20px;
    text-decoration: none;
    border-radius: 5px;    
    transition: text-shadow 0.3s ease-in-out;
    cursor: pointer;
}

.right-button {
    margin-left: auto;
    margin-right: 2%;
}
</style>