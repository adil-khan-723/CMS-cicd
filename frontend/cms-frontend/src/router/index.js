import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import LoginView from "../views/LoginView.vue";
import DashboardView from "../views/DashboardView.vue";
import NewPost from "../views/dashboard_components/NewPost.vue"; // ✅ Correct Path
import EntranceAnimation from '@/views/EntranceAnimation.vue'

const routes = [
  { path: "/", component: HomeView },
  { path: "/login", component: LoginView },
  { path: "/dashboard", component: DashboardView },
  { path: "/new-post", component: NewPost }, // ✅ Added NewPost Route
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: DashboardView
  },
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/entrance',
    name: 'entrance',
    component: EntranceAnimation
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// ✅ Navigation Guard: Protect Dashboard & New Post Page
router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem("access_token"); // ✅ Fixed key

  if ((to.path === "/dashboard" || to.path === "/new-post") && !isAuthenticated) {
    next("/login");
  } else {
    next();
  }
});

export default router;
