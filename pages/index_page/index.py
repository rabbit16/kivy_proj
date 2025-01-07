# -*- coding: utf-8 -*-
# @Time    : 2024/9/23 15:17
# @Author  : rabbit
# @File    : screen.py
# @Software: PyCharm
import logging
import os
import threading
import time
from operator import index
from random import random

import cv2
import requests
from jnius import autoclass
from kivy.app import App
from kivy.core.image import Texture
from kivy.graphics import Color, Ellipse, Line
from kivy.properties import ObjectProperty, ListProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.button import Button
from kivy.uix.carousel import Carousel
from kivy.uix.image import Image, AsyncImage
from kivy.uix.label import Label
from kivy.uix.camera import Camera
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.utils import platform as kivy_platform
from kivymd.tools.hotreload.app import MDApp

from custom_gestures.gesture_box import GestureBox
from settings.settings_proj import IMAGE_URL, FONT_NAME, HTTP_URL, IMG_W, IMG_H
from async_tasks.asyncio_insert_data import EventLoopWorker
from utils.user_widget import MyPopup, request_get, request_post
from utils.video_send_status.send_status_design import SendStatusDesign

from async_tasks.asyncio_insert_data import EventLoopWorker


class ImageButton(ButtonBehavior, Image):
    ...

class CarouselWidget(BoxLayout):
    image_list = ListProperty([])
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Carousel's specific attributes
        self.carousel = Carousel(direction='right', size_hint=(1, 1), loop=True)
        # Adding images
        self.add_image()  # TODO 后续要接入后台自动获取图片
        self.add_widget(self.carousel)
        Clock.schedule_interval(self.carousel.load_next, 15)
        Clock.schedule_interval(self.update_images_from_server,
                                15)
        # self.slides = IMAGE_URL
    def add_image(self):
        for url in IMAGE_URL:
            image = AsyncImage(source=url, fit_mode="fill")
            self.image_list.append(image)
            self.carousel.add_widget(image)
    def update_images_from_server(self, *args):
        try:
            # 示例：假设从服务器获取图片URL列表
            if MDApp.get_running_app().login_user is None or MDApp.get_running_app().is_setting is None:
                return
            response = request_get(f'{HTTP_URL}/banner/?employee_number={MDApp.get_running_app().login_user}')  #
            image_urls = response.json()  # 假设返回一个包含图片URL的列表

            # 清空旧的图片
            self.carousel.clear_widgets()

            # 添加新的图片到轮播
            for data in image_urls:
                r = request_get(data['url'])
                with open(f"{os.getcwd()}/static/proj_img/{data['filename']}", 'wb') as f:
                    f.write(r.content)
                image = Image(source=f"{os.getcwd()}/static/proj_img/{data['filename']}",
                              allow_stretch=True, keep_ratio=False)
                self.carousel.add_widget(image)
            self.carousel.load_next()
            print("Images updated from server")

        except Exception as e:
            print(f"Failed to update images from server: {e}")


class CameraModule(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.user_camera = None
        self.camera_list = []
        self.camera_list_obj = []
        self.camera_index = 0
        self.camera_dict = {}
        if kivy_platform != 'android':
            self.user_camera = self.get_available_cameras()
            # for i in self.user_camera:
            #     c = Camera(resolution=(1920, 1080), fit_mode="fill", play=True, index=i)
            #     # c = Image(source="static/proj_img/add_pic.jpg", fit_mode="fill")
            #     self.add_widget(c)
            #     Clock.schedule_interval(lambda dt: self.update(dt,+ i), 1)  # 30 FPS
            #     # threading.Thread(target=self.update, args=(i,), daemon=True).start()
            #     self.camera_list.append(c)
        else:
            self.user_camera = self.list_cameras()
        for i in self.user_camera:
            c = Camera(resolution=(1920, 1080), fit_mode="fill", play=True, index=i)
            self.add_widget(c)
            # Clock.schedule_interval(lambda dt: self.transport_pic(i), 1/30)  # 30 FPS
            # threading.Thread(target=self.update, args=(i,), daemon=True).start()
            self.camera_list.append(c)
            self.camera_dict[str(i)] = c  # 注册相机

            Clock.schedule_interval(lambda dt : self.transport_pic(i), 1 / 30)  # 30 FPS
            Clock.schedule_interval(lambda dt : self.analysis_pic(), 4)  # 30 FPS
            Clock.schedule_interval(lambda dt : self.analysis_rubbish(), 10)


        MDApp.get_running_app().camera_list = self.user_camera  # 相机列表
        MDApp.get_running_app().camera_list_obj = self.camera_list  # 没用到
        MDApp.get_running_app().camera_dict = self.camera_dict  # 相机字典
        self.register_device_info()
        self.monitor_camera()
        self.monitor_person()
        self.monitor_rubbish()
    def register_device_info(self):
        self.event_loop_worker = worker = EventLoopWorker("register_device")
        worker.start()
        print("运行注册机制结束")

    def monitor_camera(self):
        self.event_loop_worker = worker = EventLoopWorker("start_monitor_camera")
        worker.start()
        print("运行注册机制结束")

    def monitor_person(self):
        self.event_loop_worker = worker = EventLoopWorker("start_monitor_person")
        worker.start()
        print("运行注册机制结束")

    def monitor_rubbish(self):
        self.event_loop_worker = worker = EventLoopWorker("start_monitor_rubbish")
        worker.start()
        print("运行注册机制结束")

    def on_press(self):
        self.c.play = not self.c.play

    def list_cameras(self):
        # CameraManager = autoclass('android.hardware.camera2.CameraManager')
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        activity = PythonActivity.mActivity
        camera_manager = activity.getSystemService(PythonActivity.CAMERA_SERVICE)
        camera_id_list = camera_manager.getCameraIdList()
        print(camera_id_list)
        return camera_id_list
    def get_available_cameras(self, max_cameras=5):
        available_cameras = []
        for i in range(max_cameras):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                available_cameras.append(i)
                cap.release()  # 释放摄像头
        return available_cameras

    def transport_pic(self, index):
        index = str(index)
        pic = self.camera_dict[str(index)].export_as_image(size=(IMG_W, IMG_H))
        if index == str(self.user_camera[0]):
            if MDApp.get_running_app().camera_0_is_sending:
                MDApp.get_running_app().queue_camera_0.put([pic.texture.pixels, pic])
        elif index == 1:
            if MDApp.get_running_app().camera_1_is_sending:
                MDApp.get_running_app().queue_camera_1.put([pic.texture.pixels, pic])
        return True
    def analysis_pic(self):
        logging.info("正在调用摄像头")
        pic = self.camera_list[0].export_as_image(size=(IMG_W, IMG_H))
        # logging.info(f"图片信息： {pic.texture.pixels}")
        if MDApp.get_running_app().login_user and MDApp.get_running_app().is_setting:
            logging.info("开始发送图片")
            MDApp.get_running_app().queue_pic.put([pic.texture.pixels, pic])

            print("发送成功一张图")

        else:
            print("监控图片的等待登录")
        return True

    def analysis_rubbish(self):
        logging.info("正在调用摄像头")
        pic = self.camera_list[-1].export_as_image(size=(IMG_W, IMG_H))
        # logging.info(f"图片信息： {pic.texture.pixels}")
        if MDApp.get_running_app().login_user and MDApp.get_running_app().is_setting:
            logging.info("开始发送图片")
            MDApp.get_running_app().queue_pic2.put([pic.texture.pixels, pic])

            print("发送成功一张图")

        else:
            print("监控图片的等待登录")
        return True

    def update(self, index):
        camera = cv2.VideoCapture(index)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.camera_list_obj.append(camera)
        while True:
            ret, frame = camera.read()  # 读取摄像头的当前帧
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # 在主线程中更新纹理
                Clock.schedule_once(lambda dt: self.update_texture(index, frame))  # 这是合法的

    def update_texture(self, index, frame):
        # 创建一个 Kivy Texture 对象
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
        # 将图像数据传递给 Texture
        texture.blit_buffer(frame.tobytes(), colorfmt='rgb', bufferfmt='ubyte')
        # 更新对应 Image 的 texture
        self.camera_list[index].texture = texture
class LabelChina(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_name = FONT_NAME
        self.text_size
        self.halign = 'center'  # 左对齐
        self.valign = 'center'  # 垂直居中（根据需求调整）
        # self.size_hint = (1, None),
        # self.text_size = (self.width, None),

class TableData(BoxLayout):
    data_items = ListProperty([])
    """
    [
        "干垃圾每日重量",
        "是垃圾每日重量",
        "可回收物每日重量",
        "有害垃圾每日重量",
        "每日投放频次"
    ]
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.data_items = [
            "每日投放人次: ",
            "0",
            "",
            "",
            "",
            "",
        ]


class ImageSetting(Image):
    def __init__(self, img_data, rotate=0, **kwargs):
        super().__init__(**kwargs)  # 调用Image的构造函数
        self.texture = img_data.texture  # 更新图像组件的纹理

        self.check_pos_list = []  # 存储点击的位置
        # self.fit_mode = 'fill'

    def on_touch_down(self, touch):
        # 检查触摸是否在图像范围内
        if self.collide_point(touch.x, touch.y):
            # 将窗口坐标转化为小部件坐标
            img_touch_x, img_touch_y = self.to_widget(touch.x, touch.y, relative=True)

            # 计算相对于图片左上角的位置
            # img_touch_x 和 img_touch_y 是相对于当前widget左上角的坐标
            # 这里假设 img_touch_x 和 img_touch_y 的范围是在图片的宽度和高度之间
            texture_x = img_touch_x
            texture_y = self.height - img_touch_y  # 反转Y坐标，以符合纹理坐标的标准

            print("Touch at image location: ({}, {})".format(texture_x, texture_y))

            # 绘制点击点
            color = (random(), 1, 1)
            with self.canvas:
                Color(*color, mode='hsv')
                d = 15.
                Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))

            # 存储点击的位置
            self.check_pos_list.append((texture_x, texture_y))
            # print(self.check_pos_list)


class PopUpImageClick(BoxLayout):
    def __init__(self, **kwargs):
        self.size = (1, 1)
        super().__init__(**kwargs)


class ImageWeiXin(ButtonBehavior, Image):
    root_obj = ObjectProperty(None)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.press_count = 0

    def on_release_upload(self, image_self):
        data = image_self.check_pos_list
        # print(data)
        r = request_post(f"{HTTP_URL}/pic_position/", json_data={
            "employee_number": MDApp.get_running_app().login_user,
            "position": data
        })
        # print(r.json())
        # 这里是调整摄像头的结构，保证第一个摄像头是对外的摄像头
        c = MDApp.get_running_app().camera_list.pop(self.press_count % len(MDApp.get_running_app().camera_dict))
        MDApp.get_running_app().camera_list.insert(0, c)
        c2 = MDApp.get_running_app().camera_list_obj.pop(self.press_count % len(MDApp.get_running_app().camera_dict ))
        MDApp.get_running_app().camera_list_obj.insert(0, c2)
        MDApp.get_running_app().is_setting = True  # 设置这个才能注册设备和上报图像
        if r.json()["errno"] == '0':
            MyPopup(title='', content=Label(text='Upload Successfully')).open()
            self.popup.dismiss()
        else:
            MyPopup(title='', content=Label(text=f'Faild {r.json()["errno"]}')).open()
            self.popup.dismiss()

    def convert_camera_pic(self, pop_content, upload_button, change_button):
        """
        这个函数一方面是用来决定哪个是前置摄像头，还有一个作用就是上传图像的坐标信息
        :param pop_content:
        :param upload_button:
        :param change_button:
        :return:
        """
        self.press_count += 1
        pop_content.clear_widgets()
        image_self = ImageSetting(MDApp.get_running_app().camera_list_obj[self.press_count % len(MDApp.get_running_app().camera_list_obj)].export_as_image(size=(IMG_W, IMG_H)))
        l = LabelChina(text="请依次点击，干垃圾桶，湿垃圾桶和有害垃圾桶的四个角的坐标。", size_hint=(1, .1))
        pop_content.add_widget(image_self)
        pop_content.add_widget(l)
        pop_content.add_widget(change_button)
        pop_content.add_widget(upload_button)
        # print("hello change")
    def on_press(self):
        # print(MDApp.get_running_app().is_login)
        # print(MDApp.get_running_app().login_user)
        # MDApp.get_running_app().camera_list_obj[0].export_to_png("./tmp.png")  # FIXME 写一个弹出界面，然后，标定垃圾桶的位置即可
        image_self = ImageSetting(MDApp.get_running_app().camera_list_obj[0].export_as_image(size=(IMG_W, IMG_H)))
        l = LabelChina(text="请依次点击，干垃圾桶，湿垃圾桶和有害垃圾桶的四个角的坐标。", size_hint=(1, .1))
        upload_button = Button(text="上传坐标", on_press=lambda x: self.on_release_upload(image_self), font_name=FONT_NAME,
               size_hint=(1, .2))
        change_button = Button(text="切换摄像头照片", on_press=lambda x: self.convert_camera_pic(pop_content, upload_button, change_button), font_name=FONT_NAME, size_hint=(1, .2))
        pop_content = PopUpImageClick(orientation='vertical')
        pop_content.add_widget(image_self)
        pop_content.add_widget(l)

        pop_content.add_widget(change_button)
        pop_content.add_widget(upload_button)
        self.popup = Popup(title='Rubbish Bin Setting',
                      content=pop_content,
                      size_hint=(None, None), size=(IMG_W, IMG_H))
        # self.add_widget(popup)
        self.popup.open()
        # print("导出好了", os.listdir())
        # 调用摄像头拍一张照片，然后给用户设置
        # if self.press_count > 3:
        #     self.root_obj.toggle_state()
        #     self.press_count = 0
        # else:
        #     self.press_count += 1
        # self.parent.on_press()

class AddPic(BoxLayout):
    def __init__(self, **kwargs):
        self.orientation = "vertical"
        self.press_count = 0
        super().__init__(**kwargs)



class IndexScreen(GestureBox):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.update_table_list()
    @staticmethod
    def login_view():
        MDApp.get_running_app().screen_manager.current = "Login"

    def update_table_list(self):
        work = EventLoopWorker("update_data_list", with_param=True, p=self.ids)
        work.start()

# class IndexApp(App):
#     def build(self):
#         return IndexScreen()
