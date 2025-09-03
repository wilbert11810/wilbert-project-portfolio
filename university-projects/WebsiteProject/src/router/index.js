import { createRouter, createWebHistory } from 'vue-router';
import Home from "../components/Home.vue";
import Expenses from "../components/Expenses.vue";
import About from "../components/About.vue";
import Login from "../components/Login.vue";
import SignUp from "../components/Signup.vue";
import News from "../components/News.vue";


const routes = [
    {path:"/cos30043/s104323659/finance-project/",component: Home},
    {path:'/cos30043/s104323659/finance-project/expenses', component: Expenses},
    {path:'/cos30043/s104323659/finance-project/about', component: About},
    {path:'/cos30043/s104323659/finance-project/signin', component: Login},
    {path:'/cos30043/s104323659/finance-project/signup', component: SignUp},
    {path:'/cos30043/s104323659/finance-project/news', component: News},
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
