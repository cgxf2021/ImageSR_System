import request from './request'

const loginApi = (data) => {
    return request.post({
        url: '/Login',
        data: data
    }, "json")
}

const registerApi = (data) => {
    return request.post({
        url: '/Register',
        data: data
    }, "json")
}

const srcnnApi = (data) => {
    return request.post({
        url: '/srcnn',
        data: data
    }, "form")
}

const srganApi = (data) => {
    return request.post({
        url: '/srgan',
        data: data
    }, "form")
}

const downloadApi = (data) => {
    return request.downloadPost({
        url: '/download',
        data: data
    }, "json")
}

const logoutApi = (data) => {
    return request.post({
        url: '/Logout',
        data: data,
    }, "json")
}


export default {
    loginApi,
    registerApi,
    srcnnApi,
    srganApi,
    downloadApi,
    logoutApi
}