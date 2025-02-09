<script setup>

</script>

<template>
    <div class="loading">
        <h1 class="chrono">Обработка...</h1>
    </div>
</template>


<style>
.loading {
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
</style>