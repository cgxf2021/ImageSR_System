import Service from './config'

const post = (config, sign) => {
    if (sign === "json") {
        return Service.ServiceJson({
            ...config,
            method: 'post',
        })
    } else if (sign === "form") {
        return Service.ServiceFormData({
            ...config,
            method: 'post',
        })
    }
}

const get = (config, sign) => {
    if (sign === "json") {
        return Service.ServiceJson({
            ...config,
            method: 'get',
        })
    } else if (sign === "form") {
        return Service.ServiceFormData({
            ...config,
            method: 'get',
        })
    }
}

const downloadPost = (config, sign) => {
    if (sign === "json") {
        return Service.ServiceJson({
            ...config,
            method: 'post',
            responseType: "arraybuffer",
        })
    } else if (sign === "form") {
        return Service.ServiceFormData({
            ...config,
            method: 'post',
            responseType: "arraybuffer",
        })
    }
}

export default {
    post,
    get,
    downloadPost
}