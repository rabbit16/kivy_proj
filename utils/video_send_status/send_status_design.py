"""
定义消息格式：
    一. 消息类型
        1. 系统消息
            require_send  请求发送消息
            finish_send  结束发送消息
            ping  存活信息
        2. 数据消息
            pic_message  图像数据
            text_message  文本数据
            json_message  json格式数据

状态定义：
    一. 初始状态  0
    二. 检查状态  1
    三. 发送图像状态  2
    四. 持续发送状态  3
"""
import asyncio
import json
from concurrent.futures import ThreadPoolExecutor
from operator import index

import cv2
import websockets
import numpy as np
import base64

from queue import Queue
from kivymd.tools.hotreload.app import MDApp


class SendStatusDesign:
    def __init__(self, url, camera_index=0, author=None, children=0):
        """
        监控相机并传输视频信号
        :param url:
        :param camera_index:
        """
        print(f"相机的index为： {camera_index}")
        self.url = url
        self.init_status = 0
        self.check_status = 1
        self.send_pic_send_status = 2
        self.is_sending = False  # 标识是否正在广播图像数据
        self.sending_user = []  # 记录当前接收的用户有哪些,用列表记录
        self.camera_index = camera_index
        self.camera = None
        self.now_status = self.init_status  # 初始化状态机状态
        self.author = author
        self.children = children
        if self.children == '0':
            self.queue = MDApp.get_running_app().queue_camera_0
        else:
            self.queue = MDApp.get_running_app().queue_camera_1
        self.status_map = {
            self.init_status: self.init_status_func,
            self.check_status: self.check_status_func,
            self.send_pic_send_status: self.send_pic_send_status_func
        }

    async def send_message_basic(self, message_type, message, ws):
        if message_type == "system":
            send_data = {
                "headers": {
                    "type": "system",
                    "message": message,
                    "author": self.author,
                },
                "body":{

                }
            }
        else:
            send_data = {
                "headers": {
                    "type": "data",
                    "message": "pic_data",
                    "author": self.author,
                },
                "body": {
                    "content": base64.b64encode(message).decode("utf-8"),
                }
            }
        await ws.send(json.dumps(send_data))

    async def receive_data(self, ws):
        data = await ws.recv()
        data_json = json.loads(data)
        if data_json["headers"]["receiver"] == self.author and data_json["headers"]["children"] == str(self.children):
            return data_json
        else:
            print("丢弃无用消息")

    async def monitor_system_message(self, ws):
        """
        该函数持续监控系统消息，并对信号量进行相应的更改，保证程序正常发送视频信号
            1. 修改发送的人员名单
        :param ws:
        :return:
        """
        while True:
            print("系统消息监控状态")
            data = await self.receive_data(ws)
            print(data)
            if MDApp.get_running_app().camera_0_is_sending or MDApp.get_running_app().camera_1_is_sending:
                if data["headers"]["receiver"] in self.sending_user:
                    if data["headers"]["message"] == "require_send":  # 重复收到请求发送消息，疑似用户重复点击，这个是要拒绝掉的
                        continue
                    elif data["headers"]["message"] == "finish_send":
                        self.sending_user.remove(data["headers"]["receiver"])
                        if len(self.sending_user) == 0:
                            self.is_sending = False
                            if self.children == '0':
                                MDApp.get_running_app().camera_0_is_sending = False
                            else:
                                MDApp.get_running_app().camera_1_is_sending = False
                        continue
            else:
                if data is None:
                    continue
                if data["headers"]["message"] == "require_send":
                    if data["headers"]["receiver"] not in self.sending_user:
                        self.sending_user.append(data["headers"]["receiver"])
                    if self.children == '0' and MDApp.get_running_app().camera_0_is_sending:
                        continue
                    elif self.children == '1' and MDApp.get_running_app().camera_1_is_sending:
                        continue
                    else:
                        if self.children == '0':
                            MDApp.get_running_app().camera_0_is_sending = True
                        else:
                            MDApp.get_running_app().camera_1_is_sending = True
                        continue
    async def init_status_func(self, ws):
        while True:
            print("正在发送ping存活指令")
            # await self.send_message_basic("system", "ping", ws)  # 发送ping保证连接不断， 使用system链接群组
            if self.children == '0':
                if MDApp.get_running_app().camera_0_is_sending:
                    self.now_status = self.check_status
                    return self.check_status
            else:
                if MDApp.get_running_app().camera_1_is_sending:
                    self.now_status = self.check_status
                    return self.check_status
            await asyncio.sleep(1)
            continue

    async def check_status_func(self, ws):
        # self.camera = cv2.VideoCapture(self.camera_index)  # 打开摄像头或提供视频文件路径
        # self.camera = MDApp.get_running_app().camera_list_obj[self.camera_index]  # 打开摄像头或提供视频文件路径
        self.now_status = self.send_pic_send_status
        return self.send_pic_send_status

    async def send_pic_send_status_func(self, ws):
        while True:
            if not self.queue.empty() and (MDApp.get_running_app().camera_0_is_sending or MDApp.get_running_app().camera_1_is_sending):
                pic =self.queue.get()
                width, height = pic[1].width, pic[1].height
                # 获取数据，假设 pic 是 RGBA 格式
                image_data = pic[0]  # 获取图像的像素数据

                # 将数据转换为 NumPy 数组
                img_array = np.frombuffer(image_data, np.uint8).reshape((height, width, 4))

                # 将 RGBA 转换为 BGR
                img_array = cv2.cvtColor(img_array, cv2.COLOR_RGBA2BGR)
                # 编码图像为JPEG格式
                _, buffer = cv2.imencode('.jpg', img_array)
                img_as_text = buffer.tobytes()

                # 发送图像数据
                # print(img_as_text)

                await self.send_message_basic("data", img_as_text, ws)
                await asyncio.sleep(1 / 30)

                # 增加适当的延迟可以避免摄像头过载
            else:
                break
        self.is_sending = False
        self.now_status = self.init_status
        self.queue = Queue()
        if self.children == '0':
            MDApp.get_running_app().queue_camera_0 = self.queue
        else:
            MDApp.get_running_app().queue_camera_1 = self.queue
        return self.init_status
    async def keep_alive(self, ws):
        while True:
            await self.send_message_basic("system", "ping", ws)
            await asyncio.sleep(10)

    async def start_status_func(self, ws_system, ws_camera):
        while True:
            print("状态机循环状态")
            if self.now_status == self.init_status:
                await self.status_map[self.now_status](ws_system)
            else:
                await self.status_map[self.now_status](ws_camera)

    async def main(self):
        ws_system = await websockets.connect(f"{self.url}/ws/system/")  # 连接ws服务器
        ws_camera = await websockets.connect(f"{self.url}/ws/{self.author}{self.camera_index}/", ping_interval=None)
        # await asyncio.create_task(self.start_status_func(ws_system, ws_camera))
        # await asyncio.create_task(self.monitor_system_message(ws_system))
        # await asyncio.create_task(self.start_status_func(ws_system, ws_camera))
        await asyncio.gather(
            *[
                self.monitor_system_message(ws_system),
                self.start_status_func(ws_system, ws_camera),
            ]
        )


if __name__ == '__main__':
    url_system = "ws://localhost:8000"
    asyncio.run(SendStatusDesign(url_system, 0, "17511684584").main())