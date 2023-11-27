from pathlib import Path

# 后端根目录
BACK_PATH = Path("backend")
# 前端根目录
FRONT_PATH = Path("frontend")
# 前端图片资源目录
FRONT_SRC_ASSETS_IMAGES_PATH = FRONT_PATH.joinpath("src", "assets", "images")
# 后端图片资源目录
BACK_IMAGES_PATH = BACK_PATH.joinpath("images")
# srcnn模型
SRCNN_NET_PATH = BACK_PATH.joinpath("net", "srcnn_sgd_1000.h5")
# srgan模型
SRGAN_NET_PATH = BACK_PATH.joinpath("net", "gan_generator.h5")
# 数据库
HOST = '127.0.0.1'
PORT = 3306
USERNAME = 'root'
PASSWORD = '160321'
DATABASE = 'sr'