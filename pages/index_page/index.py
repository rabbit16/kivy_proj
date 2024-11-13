# -*- coding: utf-8 -*-
# @Time    : 2024/9/23 15:17
# @Author  : rabbit
# @File    : screen.py
# @Software: PyCharm
import cv2
from jnius import autoclass
from kivy.app import App
from kivy.properties import ObjectProperty, ListProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.carousel import Carousel
from kivy.uix.image import Image, AsyncImage
from kivy.uix.label import Label
from kivy.uix.camera import Camera
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.utils import platform as kivy_platform
from kivymd.tools.hotreload.app import MDApp

from custom_gestures.gesture_box import GestureBox
from settings.settings_proj import IMAGE_URL, FONT_NAME


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
        # self.slides = IMAGE_URL
    def add_image(self):
        for url in IMAGE_URL:
            image = AsyncImage(source=url, fit_mode="fill")
            self.image_list.append(image)
            self.carousel.add_widget(image)

    # def update_images_from_server(self, *args):
    #     try:
    #         # 示例：假设从服务器获取图片URL列表
    #         response = requests.get('https://example.com/api/get_images')
    #         image_urls = response.json()  # 假设返回一个包含图片URL的列表
    #
    #         # 清空旧的图片
    #         self.clear_widgets()
    #
    #         # 添加新的图片到轮播
    #         for url in image_urls:
    #             image = Image(source=url, allow_stretch=True, keep_ratio=False)
    #             self.add_widget(image)
    #
    #         print("Images updated from server")
    #
    #     except Exception as e:
    #         print(f"Failed to update images from server: {e}")


class CameraModule(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        if kivy_platform != 'android':
            use_camera = self.get_available_cameras()
            for i in use_camera:
                c = Camera(resolution=(1920, 1080), fit_mode="fill", play=True, index=i)
                self.add_widget(c)
        else:
            user_camera = self.list_cameras()
            for i in user_camera:
                c = Camera(resolution=(1920, 1080), fit_mode="fill", play=True, index=i)
                # with c.canvas.before:
                #
                #     PushMatrix()
                #     self.rotation = Rotate(angle=-90, axis=(0, 0, 1), origin=(Window.width/2+5+c.width/2, Window.height/2+5+c.height/2))
                # # # #
                # with c.canvas.after:
                #     PopMatrix()  # this method is good but origin should be smart.
                self.add_widget(c)


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
            "干垃圾每日重量",
            "12",
            "是垃圾每日重量",
            "12",
            "可回收物每日重量",
            "12",
            "有害垃圾每日重量",
            "12",
            "每日投放频次",
            "12",
            "每日投放频次",
            "12",
            "每日投放频次",
            "12",
        ]

class ImageWeiXin(ButtonBehavior, Image):
    root_obj = ObjectProperty(None)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.press_count = 0
    def on_press(self):
        print(MDApp.get_running_app().root.is_login)
        print(MDApp.get_running_app().root.login_user)
        if self.press_count > 3:
            self.root_obj.toggle_state()
            self.press_count = 0
        else:
            self.press_count += 1
        # self.parent.on_press()

class AddPic(BoxLayout):
    def __init__(self, **kwargs):
        self.orientation = "vertical"
        self.press_count = 0
        super().__init__(**kwargs)



class IndexScreen(GestureBox):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def login_view():
        MDApp.get_running_app().screen_manager.current = "Login"


# class IndexApp(App):
#     def build(self):
#         return IndexScreen()
