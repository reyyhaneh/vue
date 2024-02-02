import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import SignUp from '../components/SignUp.vue'
import Login from '../components/Login.vue'
import Profile from '../components/Profile.vue'
import UserProfile from '../components/UserProfile.vue'



const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignUp,
    }, 
    {
      path: '/profile',
      name: 'profile',
      component: Profile,
    }, 
    {
      path: '/login',
      name: 'login',
      component: Login,
    },
    {
      path: '/userProfile',
      name: 'userProfile',
      component: UserProfile,
    }
  ]
})

export default router
