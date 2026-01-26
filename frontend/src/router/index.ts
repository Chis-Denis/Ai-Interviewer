import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '../app/components/home/HomePage.vue';
import InterviewPage from '../app/components/home/InterviewPage.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomePage,
    },
    {
      path: '/interview/:id',
      name: 'interview',
      component: InterviewPage,
      props: true,
    },
  ],
});

export default router;
