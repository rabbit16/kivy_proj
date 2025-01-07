import asyncio
import base64
import threading
from concurrent.futures import ThreadPoolExecutor

import cv2
import numpy as np
import requests
from kivy.core.audio.audio_sdl2 import Clock
from kivy.event import EventDispatcher
from kivymd.app import MDApp
from settings.settings_proj import HTTP_URL, WS_BASE_URL, IMG_W, IMG_H
from utils.video_send_status.send_status_design import SendStatusDesign
import logging


class EventLoopWorker(EventDispatcher):

    # 定义唯一事件
    __events__ = ('on_pulse',)

    def __init__(self, map, with_param=False, **kwargs):
        self.p = kwargs.get("p", None)
        if self.p:
            del kwargs["p"]
        super().__init__(**kwargs)
        # 指定目标
        self._thread = threading.Thread(target=self._run_loop)
        self._thread.daemon = True
        self.loop = None
        self._pulse = None
        self._pulse_task = None
        self.map = map
        self.with_param = with_param  # 标识是否有参数传进来
        self.map_task = {
            "register_device": self.register_device,
            "update_data_list": self.update_data_list,
            "start_monitor_camera": self.start_monitor_camera,
            "start_monitor_person": self.start_monitor_person,
            "start_monitor_rubbish": self.start_monitor_rubbish,
        }


    def _run_loop(self):
        self.loop = asyncio.get_event_loop_policy().new_event_loop()
        asyncio.set_event_loop(self.loop)
        self._restart_pulse()
        self.loop.run_forever()

    def start(self):
        self._thread.start()

    async def pulse(self):
        """处理具体业务逻辑"""
        # from importfile.import_much import import_file
        logging.info("Upload is ready,filepath is %s" % self.src)
        # import_file(self.src)
        # logging.info("Upload shutdown")
        await asyncio.sleep(100)
        self.__init__(self.map)

    async def update_data_list(self, ids):
        print(asyncio.all_tasks())  # FIXME 这里接入django的后端
        while True:
            if not (MDApp.get_running_app().login_user and MDApp.get_running_app().is_setting):
                await asyncio.sleep(1)
                continue
            response = requests.get(
                f"{HTTP_URL}/message_info/?employee_number={MDApp.get_running_app().login_user}",
            )
            print(response.json())
            d = [{'text': '每日投放人次: '}, {'text': f'{response.json()[0]["execute_person"]}'},{'text': ''}
                ,{'text': ''},{'text': ''},{'text': ''},{'text': ''},{'text': ''}]
            ids.table_data_list.data = d
            await asyncio.sleep(1)

    async def start_monitor_camera(self):
        while True:
            if MDApp.get_running_app().login_user and MDApp.get_running_app().is_setting:
                break
            print("等待登录")
            await asyncio.sleep(1)
        with ThreadPoolExecutor(max_workers=2) as executor:
            for index, value in enumerate(MDApp.get_running_app().camera_list):
                print("注册了一个", index)
                # await SendStatusDesign(WS_BASE_URL, index, MDApp.get_running_app().login_user, index).main()  # 注册摄像头

                executor.submit(asyncio.run, SendStatusDesign(WS_BASE_URL, str(index),
                                                              MDApp.get_running_app().login_user, str(index)).main())

    async def start_monitor_person(self):
        while True:
            if MDApp.get_running_app().login_user and MDApp.get_running_app().is_setting:
                break
            print("等待登录 monitor person")
            logging.info("等待程序登录")
            await asyncio.sleep(1)
        while True:
            try:
                logging.info("开始监控图像队列")
                if MDApp.get_running_app().queue_pic.empty():
                    await asyncio.sleep(1)
                pic = MDApp.get_running_app().queue_pic.get(block=False)
                logging.info("正在分析图片")
                width, height = pic[1].width, pic[1].height  # 统一分析的尺寸
                # 获取数据，假设 pic 是 RGBA 格式
                image_data = pic[0]  # 获取图像的像素数据

                img_array = np.frombuffer(image_data, np.uint8).reshape((height, width, 4))

                # 将 RGBA 转换为 BGR
                img_array = cv2.cvtColor(img_array, cv2.COLOR_RGBA2BGR)
                # 编码图像为JPEG格式
                _, buffer = cv2.imencode('.jpg', img_array)
                img_as_text = buffer.tobytes()
                if pic:
                    logging.info("正在发送")
                    response = requests.post(
                        f"{HTTP_URL}/pic_person/",
                        json={
                            "employee_number": str(MDApp.get_running_app().login_user),
                            "image_data": base64.b64encode(img_as_text).decode("utf-8")
                        }
                    )
                    print(response.json())
            except Exception as e:
                logging.warning(f"报错: {e.__repr__()}")

    async def start_monitor_rubbish(self):
        while True:
            if MDApp.get_running_app().login_user and MDApp.get_running_app().is_setting:
                break
            print("等待登录 monitor person")
            logging.info("等待程序登录")
            await asyncio.sleep(1)
        while True:
            try:
                logging.info("开始监控图像队列")
                if MDApp.get_running_app().queue_pic2.empty():
                    await asyncio.sleep(1)
                pic = MDApp.get_running_app().queue_pic2.get(block=False)
                logging.info("正在分析图片")
                width, height = pic[1].width, pic[1].height  # 统一分析的尺寸
                # 获取数据，假设 pic 是 RGBA 格式
                image_data = pic[0]  # 获取图像的像素数据

                img_array = np.frombuffer(image_data, np.uint8).reshape((height, width, 4))

                # 将 RGBA 转换为 BGR
                img_array = cv2.cvtColor(img_array, cv2.COLOR_RGBA2BGR)
                # 编码图像为JPEG格式
                _, buffer = cv2.imencode('.jpg', img_array)
                img_as_text = buffer.tobytes()
                if pic:
                    logging.info("正在发送")
                    response = requests.post(
                        f"{HTTP_URL}/pic_rubbish/",
                        json={
                            "employee_number": str(MDApp.get_running_app().login_user),
                            "image_data": base64.b64encode(img_as_text).decode("utf-8")
                        }
                    )
                    print(response.json())
            except Exception as e:
                logging.warning(f"报错: {e.__repr__()}")

    def post_data(self, i):
        r = requests.post(
            url=f"{HTTP_URL}/devices/?user_phone={MDApp.get_running_app().login_user}",
            json={
                "is_delete": False,
                "device_type": 1,
                "device_name": MDApp.get_running_app().login_user,
                "device_addr": "",  # 服务端会自动填充
                "children": i
            }

        )
        print(r.json())


    async def register_device(self):
        while True:
            if MDApp.get_running_app().login_user is None:
                await asyncio.sleep(1)
                print(MDApp.get_running_app().login_user is not None)
                continue
            for i in MDApp.get_running_app().camera_list:
                Clock.schedule_once(self.post_data, i)
            self.__init__(self.map)
            break

    def _restart_pulse(self):
        """启动或重置任务"""
        if self._pulse_task is not None:
            self._pulse_task.cancel()
        if self.with_param:
            self._pulse_task = self.loop.create_task(self.map_task[self.map](self.p))
        else:
            self._pulse_task = self.loop.create_task(self.map_task[self.map]())

    def on_pulse(self, *_):
        """EventDispatcher事件必须添加的方法"""
        pass
