<template>
    <div class="outer-box" ref="outerBoxRef">
        <a ref="downloadRef" href="#" style="display: none"></a>
        <div class="page-header">
            <el-page-header @back="onBack">
                <template #content>
                    <span class="text-large font-600 mr-3"> 基于SRGAN模型的图像超分辨率重建 </span>
                </template>
                <div class="mt-4 text-sm font-bold">
                    基于SRGAN模型构建的图像超分辨率重建网页，点击下方( + )上传需要重建的图片; <br />
                    点击提交图片按钮，等待加载动画结束，重建好的图片会自动显示在界面上; <br />
                    点击下载图片按钮，将重建好的图片保存到电脑;
                </div>
            </el-page-header>
        </div>
        <div class="inner-box">
            <el-upload ref="uploadRef" v-model:file-list="fileList" action="#" list-type="picture-card"
                :on-preview="handlePictureCardPreview" :on-remove="handleRemove" :auto-upload="false"
                :on-exceed="handleExceed" :http-request="handleRequest" :limit="3">
                <el-icon>
                    <Plus />
                </el-icon>

                <template #tip>
                    <div class="el-upload__tip">
                        支持上传jpeg/png类型的图片文件，图片文件大小需要小于100kb <br />
                        最多上传3张图片
                    </div>
                </template>
            </el-upload>

            <el-button :icon="Upload" class="ml-3" type="success" @click.prevent="submitUpload">
                提交图片
            </el-button>
            <el-button :icon="Download" class="ml-3" type="success" @click.prevent="downLoadImagesZip">
                下载图片
            </el-button>
            <el-dialog v-model="dialogVisible">
                <img w-full :src="dialogImageUrl" alt="Preview Image" />
            </el-dialog>
            <div class="contrast-images">
                <div class="image-0">
                    <div class="original-div" ref="originalDivRef0">
                        <p>{{ originalImageSize[0] }}</p>
                        <img class="left-image" ref="imageRef00" :src="images[0][0]" alt="original" v-bind:title="original"
                            @mouseover="showTooltip" @mouseout="hideTooltip" />
                    </div>
                    <div class="processed-div" ref="processedDivRef0">
                        <p>{{ processedImageSize[0] }}</p>
                        <img class="right-image" ref="imageRef01" :src="images[0][1]" alt="processed"
                            v-bind:title="superResolution" @mouseover="showTooltip" @mouseout="hideTooltip" />
                    </div>
                </div>
                <div class="image-1">
                    <div class="original-div" ref="originalDivRef1">
                        <p>{{ originalImageSize[1] }}</p>
                        <img class="left-image" ref="imageRef10" :src="images[1][0]" alt="original" v-bind:title="original"
                            @mouseover="showTooltip" @mouseout="hideTooltip" />
                    </div>
                    <div class="processed-div" ref="processedDivRef1">
                        <p>{{ processedImageSize[1] }}</p>
                        <img class="right-image" ref="imageRef11" :src="images[1][1]" alt="processed"
                            v-bind:title="superResolution" @mouseover="showTooltip" @mouseout="hideTooltip" />
                    </div>
                </div>
                <div class="image-2">
                    <div class="original-div" ref="originalDivRef2">
                        <p>{{ originalImageSize[2] }}</p>
                        <img class="left-image" ref="imageRef20" :src="images[2][0]" alt="original" v-bind:title="original"
                            @mouseover="showTooltip" @mouseout="hideTooltip" />
                    </div>
                    <div class="processed-div" ref="processedDivRef2">
                        <p>{{ processedImageSize[2] }}</p>
                        <img class="right-image" ref="imageRef21" :src="images[2][1]" alt="processed"
                            v-bind:title="superResolution" @mouseover="showTooltip" @mouseout="hideTooltip" />
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
  
<script setup>
import { ref } from 'vue'
import { Plus } from '@element-plus/icons-vue'
import { ElMessage, ElLoading } from 'element-plus';
import { Upload, Download } from '@element-plus/icons-vue'
import api from '@/api/api'
import judge from '@/utils/judge'
import { useRouter } from 'vue-router'


// 图片数据列表
const fileList = ref([])
const dialogImageUrl = ref('')
const dialogVisible = ref(false)
const uploadRef = ref(null)
const imageRef00 = ref(null)
const imageRef01 = ref(null)
const imageRef10 = ref(null)
const imageRef11 = ref(null)
const imageRef20 = ref(null)
const imageRef21 = ref(null)
const imageRefs = [
    [imageRef00, imageRef01],
    [imageRef10, imageRef11],
    [imageRef20, imageRef21]
]
const images = ref(
    [
        [' ', ' '],
        [' ', ' '],
        [' ', ' ']
    ]
)
const originalImageSize = ref(['', '', ''])
const processedImageSize = ref(['', '', ''])
const originalDivRef0 = ref('')
const originalDivRef1 = ref('')
const originalDivRef2 = ref('')
const processedDivRef0 = ref('')
const processedDivRef1 = ref('')
const processedDivRef2 = ref('')
const originalDivRefs = [originalDivRef0, originalDivRef1, originalDivRef2]
const processedDivRefs = [processedDivRef0, processedDivRef1, processedDivRef2]
const outerBoxRef = ref('')
let submitOnceSign = ref(true)
const original = ref('原始的图像')
const superResolution = ref('重建后的图像')
const isTooltipVisible = ref(false)
const router = useRouter()
const imageInfoJson = ref('')
const downloadRef = ref('')

// 显示图片文字
const showTooltip = () => {
    isTooltipVisible.value = true
}
const hideTooltip = () => {
    isTooltipVisible.value = false
}

// 处理删除
const handleRemove = (uploadFile, uploadFiles) => {
    console.log(uploadFile, uploadFiles.length)
}

// 处理图片预览
const handlePictureCardPreview = (uploadFile) => {
    dialogImageUrl.value = uploadFile.url
    dialogVisible.value = true
}

// 处理图片超出
const handleExceed = () => {
    ElMessage({
        message: '最多上传3张图片',
        grouping: true,
        type: 'error',
    })
}

// 加载条
const loading = ref('')
const openFullScreen = () => {
    loading.value = ElLoading.service({
        lock: true,
        text: 'Loading',
        background: 'rgba(0, 0, 0, 0.7)',
    })
    setTimeout(() => {
        loading.value.close()
    }, 40000)
}


// 提交
const submitUpload = () => {
    let newFile = new FormData()

    if (fileList.value.length === 0) {
        ElMessage({
            message: "点击 + 上传图片",
            grouping: true,
            type: 'error',
            showClose: true
        })
    } else {
        // 找出类型不符的文件
        const badImageTypeIndex = judge.searchErrorImageType(fileList)
        // 找出大小不符的文件
        const badImageSizeIndex = judge.searchErrorImageSize(fileList, 100)

        if (badImageTypeIndex.length === 0 && badImageSizeIndex.length === 0 && submitOnceSign.value == true) {
            uploadRef.value.submit()

            // 准备提交的数据
            for (let i = 0; i < fileList.value.length; i++) {
                newFile.append(`image_${i}`, fileList.value[i].raw)
            }
            // 向后端发送请求
            api.srganApi(newFile).then(
                ElMessage({
                    message: '提交成功！',
                    grouping: true,
                    type: 'success',
                    showClose: true
                })
            ).then(
                // 加载条
                openFullScreen()
            ).then(res => {
                imageInfoJson.value = res.data
                submitOnceSign.value = false
                console.log("后端传回来的json数据", res.data)
                loading.value.close()
                for (let i = 0; i < res.data.length; i++) {
                    imageRefs[i][0].value.style.display = 'inline'
                    imageRefs[i][1].value.style.display = 'inline'
                    images.value[i][0] = require('@/assets/images/' + res.data[i].name.original)
                    images.value[i][1] = require('@/assets/images/' + res.data[i].name.processed)
                    let height = res.data[i].size.processed[0]
                    let width = res.data[i].size.processed[1]
                    width = Math.floor(250 / height * width)
                    height = 250
                    imageRefs[i][0].value.style.height = height + "px"
                    imageRefs[i][0].value.style.width = width + "px"
                    imageRefs[i][1].value.style.height = height + "px"
                    imageRefs[i][1].value.style.width = width + "px"
                    originalImageSize.value[i] = 'size: ' + res.data[i].size.original[0] + 'x' + res.data[i].size.original[1]
                    processedImageSize.value[i] = 'size: ' + res.data[i].size.processed[0] + 'x' + res.data[i].size.processed[1]
                    originalDivRefs[i].value.style.display = "inline-block"
                    processedDivRefs[i].value.style.display = "inline-block"
                }
                outerBoxRef.value.style.height = res.data.length > 2 ? "auto" : "150vh"
            }).catch(error => {
                console.log(error)
            })
        } else {
            if (submitOnceSign.value == false) {
                ElMessage({
                    message: `不能重复提交，请刷新后重新提交`,
                    grouping: true,
                    type: 'error',
                    showClose: true
                })
            }
            if (badImageTypeIndex.length > 0) {
                ElMessage({
                    message: `这些图片不是jpeg/png格式: ${badImageTypeIndex}`,
                    grouping: true,
                    type: 'info',
                    showClose: true
                })
            }
            if (badImageSizeIndex.length > 0) {
                ElMessage({
                    message: `这些图片大小超过100kb: ${badImageSizeIndex}`,
                    grouping: true,
                    type: 'info',
                    showClose: true
                })
            }
        }
    }
}

const onBack = () => {
    router.push('/Home')
}

const downLoadImagesZip = () => {
    if (imageInfoJson.value === '') {
        ElMessage({
            message: `图片列表为空`,
            grouping: true,
            type: 'error',
            showClose: true
        })
    } else {
        api.downloadApi(imageInfoJson).then(res => {
            const blob = new Blob([res.data])
            const blobUrl = window.URL.createObjectURL(blob)
            downloadRef.value.href = blobUrl
            downloadRef.value.setAttribute("download", "images.zip")
            downloadRef.value.click()
        })
    }
}

const handleRequest = () => {

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
    height: 150vh;
    margin: 0;
    padding: 0;
    background-image: linear-gradient(to left, #eea2a2 0%, #bbc1bf 19%, #57c6e1 42%, #b49fda 79%, #7ac5d8 100%);
}

.page-header {
    padding: 20px;
}

el-page-header {
    width: auto;
    height: auto;
}

.inner-box {
    width: 1100px;
    height: auto;
    margin: 0 auto;
    padding: 20px 0px 20px 0px;
    border-radius: 10px;
    background-color: rgba(255, 255, 255, 0.4);
    border: 1px solid rgba(255, 255, 255, 0.4);
    box-shadow: 5px 5px 10px 5px rgba(0, 0, 0, 0.4);
    position: relative;
}

.ml-3 {
    margin: 20px 5px 10px 5px;
    display: inline-block;
}

.contrast-images {
    height: auto;
    width: 1000px;
    margin: 0 auto;
}

.contrast-images img {
    display: none;
    border-radius: 5%;
}

img:hover::after {
    content: attr(alt);
}

img:hover {
    cursor: pointer;
}

.left-image {
    margin: 5px 10px 10px 10px;
}

.right-image {
    margin: 5px 10px 10px 10px;
}

.contrast-images p {
    margin: auto 0;
    text-align: center;
    font-size: smaller;
    font-family: 'Courier New', Courier, monospace;
    font-weight: 650;
    font-style: italic;
}

.original-div {
    display: none;
    width: auto;
    height: auto;
    margin-top: 5px;
    margin-bottom: 5px;
}

.processed-div {
    display: none;
    width: auto;
    height: auto;
    margin-top: 5px;
    margin-bottom: 5px;
}
</style>
  