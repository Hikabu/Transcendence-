import { createRouter, createWebHistory } from 'vue-router';
import LoginPage from '@/pages/LoginPage/LoginPage.vue';
import Game from '@/features/Game/Game.vue';
import Game from '@/features/Menu/Menu.vue';
import RegisterPage from '@/pages/RegisterPage/RegisterPage.vue';
import NotFound from '@/pages/NotFound.vue';
// import { useAuthStore } from '@/store/auth';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'Login',
      component: LoginPage,
      meta: { requiresAuth: false }
    },
    {
      path: '/register',
      name: 'Register',
      component: RegisterPage,
      meta: { requiresAuth: false }
    },
    {
      path: '/menu',
      name: 'Menu',
      component: Menu,
      meta: { requiresAuth: true }
    },
    {
      path: '/game',
      name: 'Game',
      component: Game,
      meta: { requiresAuth: false }
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'NotFound',
      component: NotFound
    }
  ]
});

router.beforeEach((to, from, next) => {
  // const authStore = useAuthStore();
  const isAuthenticated = localStorage.getItem('isAuthenticated') === 'true';
  
  if (to.meta.requiresAuth && !isAuthenticated) {
    console.log(to.meta.requiresAuth);
    console.log(localStorage.getItem('isAuthenticated'));
    console.log("we fucked up");
    next('/');
  } else if (to.meta.requiresAuth === false && isAuthenticated) {
    next('/menu');
  } else {
    next();
  }
});

export default router;