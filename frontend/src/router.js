import { createRouter, createWebHashHistory } from 'vue-router';
import SettingsComponent from './components/SettingsComponent.vue';

const routes = [
  {
    path: '/settings',      // URL адрес
    name: 'Settings',
    component: SettingsComponent,
  },
  {
    path: '/:pathMatch(.*)*', // Маршрут для 404 страниц
    name: 'NotFound',
    component: () => import('./components/SettingsComponent.vue'),
  },
];

// Создаём маршрутизатор
const router = createRouter({
  history: createWebHashHistory(), // Используем HTML5 history API
  routes,
});

export default router;