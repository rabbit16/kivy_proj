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
FONT_NAME = f"{PROJ_ADDR}/static/fonts/DroidSansFallback.ttf"

HTTP_URL = "http://127.0.0.1:8000"