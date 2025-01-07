# -*- coding: utf-8 -*-
# @Time    : 2024/9/24 10:30
# @Author  : rabbit
# @File    : settings_proj.py
# @Software: PyCharm
import os

PROJ_ADDR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

IMAGE_URL = [f"{PROJ_ADDR}/static/proj_img/rubbish.jpg", f"{PROJ_ADDR}/static/proj_img/rubbish2.jpg"]
INDEX_KV_PATH = f"{PROJ_ADDR}/pages/index_page/index.kv"
LOGIN_KV_PATH = f"{PROJ_ADDR}/pages/login_page/login_page.kv"
TASK_KV_PATH = f"{PROJ_ADDR}/pages/task_list_page/task_page.kv"
DEVICE_KV_PATH = f"{PROJ_ADDR}/pages/devices_list_page/device_page.kv"
FONT_NAME = f"{PROJ_ADDR}/static/fonts/DroidSansFallback.ttf"
# WS_BASE_URL = "ws://localhost:8000"
WS_BASE_URL = "ws://113.44.87.161"

# HTTP_URL = "http://127.0.0.1:8000"
HTTP_URL = "http://113.44.87.161"

IS_MOBILE = True  # 装在手机上
IMG_W, IMG_H = 640, 480  # 图像的大小