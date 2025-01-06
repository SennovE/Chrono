import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Welcome',
    component: () => import('../templates/start/index.vue')
  },
  {
    path: '/calendar',
    name: 'Calendar Page',
    component: () => import('../templates/calendar/index.vue')
  },
  {
    path: '/404',
    name: '404',
    component: () => import('../templates/Error404/index.vue')
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/404'
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router