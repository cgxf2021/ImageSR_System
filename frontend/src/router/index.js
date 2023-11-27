import COOKIE_KEY from '@/store/key';
import cookies from '@/utils/cookies';
import { ElMessage } from 'element-plus';
import { createRouter, createWebHashHistory } from 'vue-router'


const routes = [{
        path: '/',
        name: 'root',
        redirect: '/Login'
    },
    {
        path: '/Login',
        name: 'login',
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () =>
            import ( /* webpackChunkName: "about" */ '../views/Login.vue')
    },
    {
        path: '/Home',
        name: 'home',
        meta: { requiresAuth: true },
        component: () =>
            import ( /* webpackChunkName: "about" */ '../views/Home.vue')
    },
    {
        path: '/srcnn',
        name: 'srcnn',
        meta: { requiresAuth: true },
        component: () =>
            import ( /* webpackChunkName: "about" */ '../views/srcnn.vue')
    },
    {
        path: '/srgan',
        name: 'srgan',
        meta: { requiresAuth: true },
        component: () =>
            import ( /* webpackChunkName: "about" */ '../views/srgan.vue')
    },
]

const router = createRouter({
    history: createWebHashHistory(),
    routes
})


router.beforeEach((to, from, next) => {
    // 判断该路由是否需要登录权限
    if (to.matched.some(record => record.meta.requiresAuth)) {
        // 判断当前用户的登录状态
        if (cookies.getCookie(COOKIE_KEY)) {
            // 已登录，放行路由
            next();
        } else {
            // 未登录，跳转到登录页面
            ElMessage({
                message: '跳转到该页面需要完成登录',
                grouping: true,
                type: 'error',
                showClose: true
            })
            next({ name: 'login' });
        }
    } else {
        // 不需要登录权限，放行路由
        next();
    }
});

export default router