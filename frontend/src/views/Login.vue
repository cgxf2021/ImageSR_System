<template>
    <div class="bigBox">
        <div class="box">
            <!-- 滑块 -->
            <div class="pre-box" ref="preRef">
                <h1>WELCOME</h1>
                <p>SR Reconstruction</p>
                <div class="img-box">
                    <img :src="preImg" alt="">
                </div>
            </div>
            <!-- 注册 -->
            <div class="register-form">
                <!-- 标题 -->
                <div class="title-box">
                    <h1>注册</h1>
                </div>
                <!-- 输入框 -->
                <el-form :model="registerForm" :rules="rules" ref="registerFormRef" class="el-form" label-width="10px">
                    <el-form-item prop="username" label=" ">
                        <el-input type="text" placeholder="用户名" v-model="registerForm.username" :prefix-icon="User" />
                    </el-form-item>
                    <el-form-item prop="password" label=" ">
                        <el-input type="password" placeholder="密码" v-model="registerForm.password" :prefix-icon="Lock"
                            show-password />
                    </el-form-item>
                    <el-form-item prop="confirmPassword" label=" ">
                        <el-input type="password" placeholder="确认密码" v-model="registerForm.confirmPassword"
                            :prefix-icon="Lock" show-password />
                    </el-form-item>
                </el-form>
                <!-- 按钮 -->
                <div class="btn-box">
                    <button @click="register">注册</button>
                    <!-- 绑定点击事件 -->
                    <p @click="mySwitch">已有账号?去登录</p>
                </div>
            </div>
            <!-- 登录 -->
            <div class="login-form">
                <!-- 标题 -->
                <div class="title-box">
                    <h1>登录</h1>
                </div>
                <!-- 输入框 -->
                <el-form :model="loginForm" :rules="rules" ref="loginFormRef" class="el-form" label-width="5px">
                    <el-form-item prop="username" label=" ">
                        <el-input type="text" placeholder="用户名" v-model="loginForm.username" :prefix-icon="User" />
                    </el-form-item>
                    <el-form-item prop="password" label=" ">
                        <el-input type="password" placeholder="密码" v-model="loginForm.password" :prefix-icon="Lock"
                            show-password />
                    </el-form-item>
                </el-form>
                <!-- 按钮 -->
                <div class="btn-box">
                    <button @click="login">登录</button>
                    <!-- 绑定点击事件 -->
                    <p @click="mySwitch">没有账号?去注册</p>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { Lock, User } from '@element-plus/icons-vue'
import api from '@/api/api.js'
import { ElMessage } from 'element-plus';
import { useRouter } from 'vue-router';
import cookie from '@/utils/cookies.js';
import COOKIE_KEY from '@/store/key.js'
import state from '@/store/auth';

const preRef = ref('')
const imageList = [require('@/assets/cover/sr_smile.jpg'), require('@/assets/cover/smile.jpg')]
let flag = ref(true)
let preImg = ref(imageList[0])
const mySwitch = () => {
    if (flag.value) {
        preRef.value.style.background = '#57c6e1'
        preRef.value.style.transform = 'translateX(100%)'
        preImg.value = imageList[1]
    } else {
        preRef.value.style.background = '#7ac5d8'
        preRef.value.style.transform = 'translateX(0%)'
        preImg.value = imageList[0]
    }
    flag.value = !flag.value
}

// 表单操作
const loginForm = reactive({
    username: '',
    password: ''
})
const loginFormRef = ref()

const registerForm = reactive({
    username: '',
    password: '',
    confirmPassword: ''
})

const registerFormRef = ref()

// 用户名验证
const validateUsername = (rule, value, callback) => {
    if (value === '') {
        callback(new Error('用户名不能为空'))
    } else if (value.length < 6) {
        callback(new Error('用户名必须大于等于6个字符'))
    } else {
        callback()
    }
}

// 密码验证
const validatePassword = (rule, value, callback) => {
    if (value === '') {
        callback(new Error('密码不能为空'))
    } else if (value.length < 8) {
        callback(new Error('密码必须大于等于8个字符'))
    } else {
        callback()
    }
}

// 确认密码验证
const validateConfirmPassword = (rule, value, callback) => {
    if (value === '') {
        callback(new Error('确认密码不能为空'))
    } else if (value !== registerForm.password) {
        callback(new Error("确认密码与密码不匹配"))
    } else {
        callback()
    }
}

// 验证规则
const rules = reactive({
    username: [
        { validator: validateUsername, trigger: 'blur' },
    ],
    password: [
        { validator: validatePassword, trigger: 'blur' },
    ],
    confirmPassword: [
        { validator: validateConfirmPassword, trigger: 'blur' },
    ],
})

// 将登录表单发送至后端接口
const router = useRouter()
const login = () => {
    loginFormRef.value.validate((valid) => {
        if (valid) {
            api.loginApi(loginForm).then(res => {
                console.log('login', res)
                if (res.data === "登录成功") {
                    ElMessage({
                        message: '登录成功！',
                        grouping: true,
                        type: 'success',
                    })
                    // 添加cookie
                    state.isLogin = true
                    state.user = loginForm.username
                    cookie.setCookie(COOKIE_KEY, JSON.stringify(state), 1)
                    // 跳转至主页面
                    router.push('/Home')
                } else {
                    ElMessage({
                        message: '登录失败！',
                        grouping: true,
                        type: 'error',
                    })
                }
            }).catch(error => {
                console.log(error)
            })
        }
    })
}

// 将注册表单发送至后端接口
const register = () => {
    registerFormRef.value.validate((valid) => {
        if (valid) {
            api.registerApi(registerForm).then(res => {
                console.log("register", res)
                if (res.data === "注册成功") {
                    ElMessage({
                        message: "注册成功！",
                        grouping: true,
                        type: 'success',
                    })
                } else {
                    ElMessage({
                        message: "注册失败！",
                        grouping: true,
                        type: 'error'
                    })
                }
            }).catch(error => {
                console.log(error)
            })
        }
    })
}

</script>

<style>
* {
    /* 去除浏览器默认内外边距 */
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

.bigBox {
    height: 100vh;
}

.bigBox {
    /* 溢出隐藏 */
    overflow-x: hidden;
    display: flex;
    /* 渐变方向从左到右 */
    background-image: linear-gradient(to left, #eea2a2 0%, #bbc1bf 19%, #57c6e1 42%, #b49fda 79%, #7ac5d8 100%);
}

/* 最外层的大 */
.box {
    width: 1050px;
    height: 600px;
    display: flex;
    /* 相对定位 */
    position: relative;
    z-index: 2;
    margin: auto;
    /* 设置圆角 */
    border-radius: 8px;
    /* 设置边框 */
    border: 1px solid rgba(255, 255, 255, .6);
    /* 设置阴影 */
    box-shadow: 2px 1px 19px rgba(0, 0, 0, .1);
}

/* 滑动的 */
.pre-box {
    /* 宽度为大的一半 */
    width: 50%;
    /* width: var(--width); */
    height: 100%;
    /* 绝对定位 */
    position: absolute;
    /* 距离大左侧为0 */
    left: 0;
    /* 距离大顶部为0 */
    top: 0;
    z-index: 99;
    border-radius: 4px;
    background-color: #edd4dc;
    box-shadow: 2px 1px 19px rgba(0, 0, 0, .1);
    /* 动画过渡，先加速再减速 */
    transition: 0.5s ease-in-out;
}

/* 滑动的标题 */
.pre-box h1 {
    margin-top: 150px;
    text-align: center;
    /* 文字间距 */
    letter-spacing: 5px;
    color: white;
    /* 禁止选中 */
    user-select: none;
    /* 文字阴影 */
    text-shadow: 4px 4px 3px rgba(0, 0, 0, .1);
}

/* 滑动的文字 */
.pre-box p {
    height: 30px;
    line-height: 30px;
    text-align: center;
    margin: 20px 0;
    /* 禁止选中 */
    user-select: none;
    font-weight: bold;
    color: white;
    text-shadow: 4px 4px 3px rgba(0, 0, 0, .1);
}

/* 图片 */
.img-box {
    width: 200px;
    height: 200px;
    margin: 20px auto;
    /* 设置为圆形 */
    border-radius: 50%;
    /* 设置用户禁止选中 */
    user-select: none;
    overflow: hidden;
    box-shadow: 4px 4px 3px rgba(0, 0, 0, .1);
}

/* 图片 */
.img-box img {
    width: 100%;
    transition: 0.5s;
}

/* 登录和注册 */
.login-form,
.register-form {
    flex: 1;
    height: 100%;
}

/* 标题 */
.title-box {
    height: 300px;
    line-height: 500px;

}

/* 标题 */
.title-box h1 {
    text-align: center;
    color: white;
    /* 禁止选中 */
    user-select: none;
    letter-spacing: 5px;
    text-shadow: 4px 4px 3px rgba(0, 0, 0, .1);

}

/* 输入框 */
.el-form {
    display: flex;
    /* 纵向布局 */
    flex-direction: column;
    /* 水平居中 */
    align-items: center;
}

.el-form-item {
    width: 65%;
}

/* 输入框 */
/* el-input {
    width: 100%;
    height: 40px;
    margin-bottom: 20px;
    text-indent: 10px;
    border: 1px solid #fff;
    background-color: rgba(255, 255, 255, 0.3);
    border-radius: 120px;
    backdrop-filter: blur(10px);
    outline: none;
    color: #b0cfe9;
} */


/* 聚焦时隐藏文字 */
/* el-input:focus::placeholder {
    opacity: 0;
} */

/* 按钮 */
.btn-box {
    display: flex;
    justify-content: center;
}

/* 按钮 */
button {
    width: 100px;
    height: 30px;
    margin: 0 7px;
    line-height: 30px;
    border: none;
    border-radius: 4px;
    background-color: #69b3f0;
    color: white;
}

/* 按钮悬停时 */
button:hover {
    /* 鼠标小手 */
    cursor: pointer;
    /* 透明度 */
    opacity: .8;
}

/* 按钮文字 */
.btn-box p {
    height: 30px;
    line-height: 30px;
    /* 禁止选中 */
    user-select: none;
    font-size: 14px;
    color: white;

}

.btn-box p:hover {
    cursor: pointer;
    border-bottom: 1px solid white;
}
</style>