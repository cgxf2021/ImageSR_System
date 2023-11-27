from flask import Flask, request, send_file
from flask_cors import CORS
from config import BACK_PATH
from utils import ImageOperation, UserOperation
import time
import zipfile
from pathlib import Path

image_operation = ImageOperation()

app = Flask(__name__)

# 跨域问题
cors = CORS(app)


@app.route('/')
def hello_world():
    return 'hello world'


@app.route('/Login', methods=['POST'])
def login():
    login_form = request.json
    print(login_form["username"], login_form["password"])
    user_operation = UserOperation()
    sign = user_operation.check_login(user=login_form["username"], pwd=login_form["password"])
    return sign


@app.route('/Register', methods=['POST'])
def register():
    register_form = request.json
    print(register_form["username"], register_form["password"],
          register_form["confirmPassword"])
    user_operation = UserOperation()
    sign = user_operation.check_register(user=register_form["username"], pwd=register_form["password"])
    return sign


@app.route('/Logout', methods=['POST'])
def logout():
    logout_form = request.json
    print(logout_form["user"])
    user_operation = UserOperation()
    sign = user_operation.check_logout(user=logout_form["user"])
    return sign


@app.route('/srcnn', methods=['POST'])
def use_srcnn():
    return_json = list()
    # image_operation = ImageOperation()
    images = request.files.to_dict()
    image_operation.delete_image()
    # 图像重建
    for key in images.keys():
        prefix = key
        suffix = ''
        if images[key].content_type == "image/jpeg":
            suffix = "jpg"
        else:
            suffix = "png"
        image_operation.save_original_image_to_back(
            image_storage=images[key], prefix=key)
        original_image = image_operation.read_original_image_from_back(
            prefix=prefix, suffix=suffix)
        image_operation.save_image_to_front(
            image=original_image, prefix=prefix, suffix=suffix, dir_name="original_srcnn")
        processed_image = image_operation.process_image_by_model(
            model_name='srcnn', image=original_image)
        image_operation.save_image_to_front(
            image=processed_image, prefix='sr_' + prefix, suffix=suffix, dir_name="processed_srcnn")
        # 返回前端的数据
        return_json.append({
            "name": {
                "original": "original_srcnn/" + prefix + '.' + suffix,
                "processed": "processed_srcnn/" + "sr_" + prefix + '.' + suffix
            },
            "size": {
                "original": original_image.shape,
                "processed": processed_image.shape
            }
        })
    time.sleep(5)
    return return_json


@app.route('/srgan', methods=['POST'])
def use_srgan():
    return_json = list()
    # image_operation = ImageOperation()
    images = request.files.to_dict()
    image_operation.delete_image()
    # 图像重建
    for key in images.keys():
        prefix = key
        suffix = ''
        if images[key].content_type == "image/jpeg":
            suffix = "jpg"
        else:
            suffix = "png"
        image_operation.save_original_image_to_back(
            image_storage=images[key], prefix=key)
        original_image = image_operation.read_original_image_from_back(
            prefix=prefix, suffix=suffix)
        image_operation.save_image_to_front(
            image=original_image, prefix=prefix, 
            suffix=suffix, dir_name="original_srgan")
        # 调用训练好的模型重建图像
        processed_image = image_operation.process_image_by_model(
            model_name='srgan', image=original_image)
        image_operation.save_image_to_front(
            image=processed_image, prefix='sr_' + prefix, 
            suffix=suffix, dir_name="processed_srgan")
        # 返回前端的数据
        return_json.append({
            "name": {
                "original": "original_srgan/" + prefix + '.' + suffix,
                "processed": "processed_srgan/" + "sr_" + prefix + '.' + suffix
            },
            "size": {
                "original": original_image.shape,
                "processed": processed_image.shape
            }
        })
    time.sleep(5)
    return return_json


@app.route('/download', methods=['POST'])
def download():
    # image_operation = ImageOperation()
    image_json = request.json["_rawValue"]
    zip_file_path = BACK_PATH.joinpath("images.zip")
    zip_file = zipfile.ZipFile(zip_file_path, 'w')
    for image_info in image_json:
        # 获取待下载的图片信息
        original_path = image_info["name"]["original"]
        processed_path = image_info["name"]["processed"]
        # 访问资源文件夹
        original_image_bytes = image_operation.read_image_from_front(
            image_path=original_path)
        processed_image_bytes = image_operation.read_image_from_front(
            image_path=processed_path)
        original_name = original_path.split('/')[1]
        processed_name = processed_path.split('/')[1]
        # 将图片加入压缩包
        zip_file.writestr(original_name, original_image_bytes)
        zip_file.writestr(processed_name, processed_image_bytes)
    zip_file.close()
    # 将压缩包传回前端
    return send_file(path_or_file=Path("images.zip"), as_attachment=True)


if __name__ == '__main__':
    app.run()
