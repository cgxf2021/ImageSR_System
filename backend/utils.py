from config import FRONT_SRC_ASSETS_IMAGES_PATH, BACK_IMAGES_PATH
from config import SRCNN_NET_PATH, SRGAN_NET_PATH
from config import USERNAME, PORT, HOST, PASSWORD, DATABASE
from model import SRCNN, generator
import cv2
import pymysql
import tensorflow as tf
import numpy as np


def resolve(model, lr_batch):
    lr_batch = tf.cast(lr_batch, tf.float32)
    sr_batch = model(lr_batch)
    sr_batch = tf.clip_by_value(sr_batch, 0, 255)
    sr_batch = tf.round(sr_batch)
    sr_batch = tf.cast(sr_batch, tf.uint8)
    return sr_batch


def resolve_single(model, lr):
    return resolve(model, tf.expand_dims(lr, axis=0))[0]


def try_gpu(i=0):
    """Return gpu(i) if exists, otherwise return cpu().

    Defined in :numref:`sec_use_gpu`"""
    if len(tf.config.experimental.list_physical_devices('GPU')) >= i + 1:
        return tf.device(f'/GPU:{i}')
    return tf.device('/CPU:0')


def crop_image(image, factor):
    """ 裁剪图片 """
    image_h, image_w, _ = image.shape
    image_h_1 = (image_h // factor) * factor
    image_w_1 = (image_w // factor) * factor

    return image[0: image_h_1, 0: image_w_1, :]


def srcnn_resolve(model, original_img, factor=3):
    # 裁剪图片
    cropped_image = crop_image(image=original_img, factor=factor)
    img_h, img_w, _ = cropped_image.shape
    # 放大
    cropped_image = cv2.resize(src=cropped_image, dsize=(
        img_w * factor, img_h * factor), interpolation=cv2.INTER_CUBIC)
    # bgr to yuv
    original_img = cv2.cvtColor(src=cropped_image, code=cv2.COLOR_BGR2YUV)
    # 处理y通道
    original_img_y = np.expand_dims(original_img[:, :, 0], axis=2)
    # y通道归一化
    original_img_y_normal = np.expand_dims(original_img_y / 127.5 - 1, axis=2)
    # 修改成输入形状
    original_img_y_input = np.expand_dims(original_img_y_normal, axis=0)
    # 输入模型
    high_img_y = np.array(model(original_img_y_input))
    # 取出y通道
    high_img_y = high_img_y[0, :, :, :]
    high_img_y[high_img_y >= 1] = 1
    high_img_y[high_img_y <= -1] = -1
    # 合并通道
    sr_img_y = (high_img_y + 1) * 127.5
    sr_img_y = sr_img_y.astype(np.uint8)
    # yuv to bgr
    original_img[:, :, 0] = sr_img_y[:, :, 0]
    sr_img = cv2.cvtColor(src=original_img, code=cv2.COLOR_YUV2BGR)

    return sr_img


class ImageOperation(object):
    def __init__(self) -> None:
        self.SAVE_FRONT_DIRECTORY = FRONT_SRC_ASSETS_IMAGES_PATH
        self.SAVE_BACK_DIRECTORY = BACK_IMAGES_PATH
        self.SRCNN_NET_PATH = SRCNN_NET_PATH
        self.SRGAN_NET_PATH = SRGAN_NET_PATH
        self.srcnn = SRCNN()
        self.srgan = generator()
        
        

    def delete_image(self):
        for path in self.SAVE_BACK_DIRECTORY.iterdir():
            path.unlink()

        for path in self.SAVE_FRONT_DIRECTORY.joinpath("original_srcnn").iterdir():
            path.unlink()

        for path in self.SAVE_FRONT_DIRECTORY.joinpath("processed_srcnn").iterdir():
            path.unlink()

        for path in self.SAVE_FRONT_DIRECTORY.joinpath("original_srgan").iterdir():
            path.unlink()
            
        for path in self.SAVE_FRONT_DIRECTORY.joinpath("processed_srgan").iterdir():
            path.unlink()

    def save_image_to_front(self, image, prefix, suffix, dir_name):
        """
        description: 保存图片到前端指定目录
        param: image: cv2图片 prefix: 保存文件名前缀 suffix: 保存文件名后缀 dir_name: 保存目录
        Returns: None
        """
        # 保存目录
        save_path = self.SAVE_FRONT_DIRECTORY.joinpath(dir_name)
        if not save_path.exists():
            save_path.mkdir()
        image_name = prefix + '.' + suffix
        cv2.imwrite(filename=str(save_path.joinpath(image_name)), img=image)

    def save_original_image_to_back(self, image_storage, prefix):
        """
        description: 保存原来的图片到后端指定目录 
        param: image_storage: storage类型文件 prefix: 保存文件名前缀
        Returns: None
        """
        # 保存目录
        save_path = self.SAVE_BACK_DIRECTORY
        if image_storage.content_type == "image/jpeg":
            image_name = prefix + ".jpg"
            image_storage.save(str(save_path.joinpath(image_name)))
        else:
            image_name = prefix + ".png"
            image_storage.save(str(save_path.joinpath(image_name)))

    def read_original_image_from_back(self, prefix, suffix):
        """
        description: 从后端指定文件夹读取原来的图片 
        param: prefix: 文件名前缀 suffix: 文件名后缀
        Returns: None
        """
        # 读取图片
        image_name = prefix + '.' + suffix
        image = cv2.imread(filename=str(
            self.SAVE_BACK_DIRECTORY.joinpath(image_name)))
        return image

    def read_image_from_front(self, image_path):
        """
        description: 从前端文件夹读取需要保存的图片 
        param: prefix: 文件名前缀 suffix: 文件名后缀
        Returns: 图片字节流
        """
        image_path = self.SAVE_FRONT_DIRECTORY.joinpath(image_path)

        return image_path.read_bytes()

    def process_image_by_model(self, model_name, image):
        """
        description: 用指定模型处理图片返回图片
        param: model_name: 模型名称 image: 图片
        Returns: 处理好的图片
        """

        with try_gpu():
            if model_name == 'srcnn':
                self.srcnn.load_model(path=self.SRCNN_NET_PATH)
                output_image = srcnn_resolve(
                    model=self.srcnn.net, original_img=image)
            elif model_name == 'srgan':
                # bgr to rgb
                self.srgan.load_weights(filepath=self.SRGAN_NET_PATH)
                image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)
                gan_image = resolve_single(self.srgan, image)
                output_image = cv2.cvtColor(
                    np.array(gan_image), cv2.COLOR_RGB2BGR)
            return output_image


class UserOperation(object):
    def __init__(self) -> None:
        self.host = HOST
        self.username = USERNAME
        self.port = PORT
        self.password = PASSWORD
        self.database = DATABASE

    def check_login(self, user, pwd):
        """
        description: 检查是否登录成功
        param: user: 用户名 pwd: 密码
        Returns: 登录成功或失败
        """
        try:
            # 创建数据库连接
            self.connection = pymysql.connect(
                host=self.host,
                user=self.username,
                port=self.port,
                passwd=self.password,
                db=self.database
            )
            # 创建一个游标对象
            cursor = self.connection.cursor()
            search_sql = f"SELECT * FROM user WHERE username = '{user}' AND password = '{pwd}';"
            update_sql = f"UPDATE user SET state = {1} WHERE username = '{user}' AND password = '{pwd}';"
            # 查询
            cursor.execute(search_sql)
            # 结果
            search_result = cursor.fetchall()
            if search_result:
                cursor.execute(update_sql)
                self.connection.commit()
                return "登录成功"
            else:
                return "登录失败"
        except Exception as e:
            # 处理异常的代码
            self.connection.rollback()
            print(f"An error occurred: {e}")
            return "登录失败"
        finally:
            cursor.close()
            self.connection.close()

    def check_logout(self, user):
        try:
            # 创建数据库连接
            self.connection = pymysql.connect(
                host=self.host,
                user=self.username,
                port=self.port,
                passwd=self.password,
                db=self.database
            )
            # 创建一个游标对象
            cursor = self.connection.cursor()
            update_sql = f"UPDATE user SET state = {0} WHERE username = '{user}';"
            # 修改状态
            cursor.execute(update_sql)
            # 提交
            self.connection.commit()
            return "登出成功"
        except Exception as e:
            # 处理异常的代码
            self.connection.rollback()
            print(f"An error occurred: {e}")
            return "登出失败"
        finally:
            cursor.close()
            self.connection.close()


    def check_register(self, user, pwd):
        try:
            # 创建数据库连接
            self.connection = pymysql.connect(
                host=self.host,
                user=self.username,
                port=self.port,
                passwd=self.password,
                db=self.database
            )
            # 创建一个游标对象
            cursor = self.connection.cursor()
            search_sql = f"SELECT * FROM user WHERE username = '{user}';"
            insert_sql = f"INSERT INTO user(username, password) VALUES ('{user}', '{pwd}');"
            # 修改状态
            cursor.execute(search_sql)
            # 结果
            search_result = cursor.fetchall()
            if search_result:
                return "注册失败"
            else:
                print("haohaohao")
                cursor.execute(insert_sql)
                self.connection.commit()
                return "注册成功"
        except Exception as e:
            # 处理异常的代码
            self.connection.rollback()
            print(f"An error occurred: {e}")
            return "注册失败"
        finally:
            cursor.close()
            self.connection.close()
