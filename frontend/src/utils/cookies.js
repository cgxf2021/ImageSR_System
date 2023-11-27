// 设置 Cookie
const setCookie = (key, value, days) => {
    const expires = new Date();
    expires.setTime(expires.getTime() + days * 24 * 60 * 60 * 1000);
    document.cookie = `${key}=${value};expires=${expires.toUTCString()};path=/`;
}

// 获取 Cookie
function getCookie(key) {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        // 如果该 cookie 的键与指定的键匹配，则返回 cookie 值
        if (cookie.startsWith(`${key}=`)) {
            const cookieValue = cookie.substring(`${key}=`.length, cookie.length);
            const cookieObject = JSON.parse(cookieValue)
            return cookieObject
        }
    }
    return null;
}

// 删除 Cookie
function deleteCookie(key) {
    setCookie(key, '', -1);
}

// 在 Vue 组件中使用
export default {
    setCookie,
    getCookie,
    deleteCookie
}