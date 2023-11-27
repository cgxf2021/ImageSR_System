import axios from "axios";

const ServiceJson = axios.create({
    baseURL: 'http://127.0.0.1:5000',
    timeout: 0,
    headers: { 'Content-Type': 'application/json' }
});

// 添加请求拦截器
ServiceJson.interceptors.request.use((config) => {
    // 在发送请求之前做些什么
    return config;
}, (error) => {
    // 对请求错误做些什么
    return Promise.reject(error);
});

// 添加响应拦截器
ServiceJson.interceptors.response.use((response) => {
    // 2xx 范围内的状态码都会触发该函数。
    // 对响应数据做点什么
    return response;
}, (error) => {
    // 超出 2xx 范围的状态码都会触发该函数。
    // 对响应错误做点什么
    return Promise.reject(error);
});


const ServiceFormData = axios.create({
    baseURL: 'http://127.0.0.1:5000',
    timeout: 0,
    headers: {
        'Content-Type': 'multipart/form-data',
    }
});

// 添加请求拦截器
ServiceFormData.interceptors.request.use((config) => {
    // 在发送请求之前做些什么
    return config;
}, (error) => {
    // 对请求错误做些什么
    return Promise.reject(error);
});

// 添加响应拦截器
ServiceFormData.interceptors.response.use((response) => {
    // 2xx 范围内的状态码都会触发该函数。
    // 对响应数据做点什么
    return response;
}, (error) => {
    // 超出 2xx 范围的状态码都会触发该函数。
    // 对响应错误做点什么
    return Promise.reject(error);
});


export default {
    ServiceJson,
    ServiceFormData
}