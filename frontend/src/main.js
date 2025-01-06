import { createApp } from 'vue'
import App from './templates/App.vue'
import router from './router';

const app = createApp(App);

app.use(router); // Используем маршрутизатор
app.mount('#app');