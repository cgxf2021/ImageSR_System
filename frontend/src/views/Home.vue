<template>
    <div class="outer-box">
        <div id="top">
            <div class="label" @click="routerLogin">LOGOUT</div>
            <div class="label" @click="routerSrcnn">SRCNN</div>
            <div class="label" @click="routerSrgan">SRGAN</div>
        </div>
        <div class="header">
            <el-carousel :interval="4000" type="card" height="300px">
                <el-carousel-item v-for="item in 3" :key="item">
                    <img :src="imageCard[item]" alt="">
                </el-carousel-item>
            </el-carousel>
        </div>
        <div class="article">
            <div class="title">基于深度学习的图像超分辨率重建系统</div>
            <div class="sr-box">
                <div class="srcnn-review">
                    SRCNN是一种深度卷积神经网络，用于超分辨率图像重建任务。SRCNN全称为"Super Resolution Convolutional Neural
                    Network"，由Dong等人在2014年提出。<span>点击右侧图片跳转至SRCNN重建页面。</span>
                </div>
                <div class="srcnn-icon">
                    <img @click="routerSrcnn" src="@/assets/cover/blue_fly.png" alt="">
                    <p @click="routerSrcnn">SRCNN</p>
                </div>
                <div class="srgan-icon">
                    <img @click="routerSrgan" src="@/assets/cover/white_flower.png" alt="">
                    <p @click="routerSrgan">SRGAN</p>
                </div>
                <div class="srgan-review">
                    SRGAN是一种基于生成对抗网络（GAN）的超分辨率图像重建算法，全称为"Super Resolution Generative Adversarial Network"。它由Christian
                    Ledig等人在2017年提出。<span>点击左侧图片跳转至SRGAN重建页面。</span>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
import cookies from '@/utils/cookies';
import COOKIE_KEY from '@/store/key';
import api from '@/api/api.js';
import { ElMessage } from 'element-plus';

const router = useRouter()

const imageCard = [require('@/assets/cover/comic.png'), require('@/assets/cover/face.png'), require('@/assets/cover/smile.png'), require('@/assets/cover/comic.png')]

const routerSrcnn = () => {
    router.push('/srcnn')
}

const routerSrgan = () => {
    router.push('/srgan')
}

const routerLogin = () => {
    // 获取cookie信息
    const user_info = cookies.getCookie(COOKIE_KEY)
    // 向后端发送登出请求
    api.logoutApi(user_info).then(res => {
        console.log('logout', res)
        if (res.data == "登出成功") {
            ElMessage({
                message: '登出成功！',
                grouping: true,
                type: 'success',
            })
            // 删除cookie
            cookies.deleteCookie(COOKIE_KEY)
            // 跳转至登录页面
            router.push('/Login')
        } else {
            ElMessage({
                message: '登出失败！',
                grouping: true,
                type: 'error',
            })
        }
    }).catch(error => {
        console.log(error)
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
</style>


<style scoped>
.outer-box {
    width: 100%;
    height: 100%;
    margin: 0;
    padding: 0;
    background-image: linear-gradient(to left, #eea2a2 0%, #bbc1bf 19%, #57c6e1 42%, #b49fda 79%, #7ac5d8 100%);

}

#top {
    height: 40px;
    width: auto;
    z-index: 1;
}

#top div {
    width: 100px;
    height: 40px;
    background-color: #3da4be;
    float: right;
    padding-top: 10px;
    padding-left: 15px;
    text-align: center;
    opacity: 0.6;
    color: rgb(245, 230, 230);
}

#top>div:nth-child(3) {
    border-bottom-left-radius: 20px;
}

.label:hover {
    cursor: pointer;
}

.header {
    height: auto;
}


.article {
    width: 100%;
    height: auto;
    display: block;
    padding: 10px 5px 50px 5px;
}

.srcnn-icon p:hover {
    cursor: pointer;
}

.srgan-icon p:hover {
    cursor: pointer;
}

.sr-box {
    /* display: flex; */
    width: 1100px;
    height: 400px;
    margin: auto;
    z-index: 1;
    /* box-shadow: 3px 3px 5px rgba(0, 0, 0, 0.4); */
    background-color: rgba(255, 255, 255, 0.4);
    border: 1px solid rgba(255, 255, 255, 0.4);
    box-shadow: 5px 5px 10px 5px rgba(0, 0, 0, 0.4);
    border-radius: 8px;
}

.title {
    margin: 20px 0px 20px 0px;
    font-size: x-large;
    font-family: 'Courier New', Courier, monospace;
    font-weight: 800;
    font-style: italic;
    text-align: center;
}

.srcnn-icon {
    display: inline-block;
    width: 300px;
    height: 350px;
    margin-top: 50px;
}

.srgan-icon {
    display: inline-block;
    width: 300px;
    height: 350px;
    margin-top: 50px;
}

.srcnn-review {
    width: 180px;
    height: 350px;
    margin-top: 75px;
    margin-left: 50px;
    float: left;
    text-align: left;
    font-style: italic;
    font-weight: 200;
}

.srgan-review {

    width: 180px;
    height: 350px;
    margin-top: 75px;
    margin-right: 50px;
    float: right;
    text-align: left;
    font-style: italic;
    font-weight: 200;
}

div span {
    font-weight: 800;
    font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
}

.sr-box img {
    width: 250px;
    height: 250px;
    z-index: 2;
    border-radius: 10px;
    opacity: 0.8;
    box-shadow: 3px 3px 5px rgba(0, 0, 0, 0.4);
    background-color: rgba(195, 189, 189, 0.4);
    border: 1px solid rgba(121, 117, 117, 0.4);
    transition: transform 1s ease-in-out;
    margin-bottom: 20px;
    margin-top: 5px;
}

.sr-box img:hover {
    transform: scale(1.2);
    cursor: pointer;
}

.sr-box p {
    width: 300px;
    height: auto;
    margin: 0 auto;
    text-align: center;
    font-size: xx-large;
}


.el-carousel__item {
    height: auto;
    border-radius: 10px;
}

.el-carousel__item img {
    color: #475669;
    opacity: 0.75;
    line-height: 300px;
    margin-top: 3px;
    border-radius: 10px;
    text-align: center;
}

.el-carousel__item:nth-child(2n) {
    background-color: #ebb5b5;
}

.el-carousel__item:nth-child(2n + 1) {
    background-color: #8eb8c3;
}
</style>
  