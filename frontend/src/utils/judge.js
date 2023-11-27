// 判断文件类型
const searchErrorImageType = (fileList) => {
    let badImageIndex = []

    for (let i = 0; i < fileList.value.length; i++) {
        if (fileList.value[i].raw.type !== "image/jpeg" && fileList.value[i].raw.type !== "image/png") {
            badImageIndex.push(i + 1)
        }
    }

    return badImageIndex
}

// 判断文件大小
const searchErrorImageSize = (fileList, limitSize) => {
    let badImageIndex = []

    for (let i = 0; i < fileList.value.length; i++) {
        if (fileList.value[i].raw.size / 1024 > limitSize) {
            badImageIndex.push(i + 1)
        }
    }
    return badImageIndex
}


export default {
    searchErrorImageType,
    searchErrorImageSize,
}