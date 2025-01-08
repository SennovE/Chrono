<script setup>
</script>

<template>
    <div class='top-nav'>
        <ul>
            <li><b><a href='#'>Главная</a></b></li>
            <li><b><a href='#'>Расписание</a></b></li>
            <li><b><a href='#'>Дедлайны</a></b></li>
            <li class='right-button'><b><a href='#'>Профиль</a></b></li>
        </ul>
    </div>
</template>

<style>
@import './LoginStile.css';

.top-nav {
    width: 100%;
    background: linear-gradient(to left, #cebeb8, #b7a098);
    position: fixed;
    top: 0;
    left: 0;
    box-shadow: 0px 0px 20px #6a6a6aa8;
}

.top-nav ul {
    display: flex;
    list-style-type: none;
    justify-content: flex-start;
}

.top-nav li a {
    display: block;
    padding: 15px 20px;
    color: #000000;
    text-decoration: none;
    border-radius: 5px;    
    transition: text-shadow 0.3s ease-in-out;
}

.right-button {
    margin-left: auto;
    padding-right: 1%;
}

</style>