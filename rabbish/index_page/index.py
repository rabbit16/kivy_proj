# -*- coding: utf-8 -*-
# @Time    : 2024/9/23 15:17
# @Author  : rabbit
# @File    : screen.py
# @Software: PyCharm
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.carousel import Carousel
from kivy.uix.image import Image, AsyncImage
from kivy.uix.label import Label
from kivy.uix.camera import Camera
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
import requests
from kivy.uix.textinput import TextInput

from settings.settings_proj import IMAGE_URL, INDEX_KV_PATH

Builder.load_file(INDEX_KV_PATH)


class StatisticsModule(BoxLayout):
    def __init__(self, **kwargs):
        super(StatisticsModule, self).__init__(**kwargs)
        self.orientation = 'vertical'

        # 示例数据
        for i in range(1, 1):  # 假设有20条统计数据
            label = Label(text=f'Statistic {i}: Data {i}', size_hint_y=None, height=30)
            self.add_widget(label)


class CarouselWidget(Carousel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Carousel's specific attributes
        self.direction = 'right'
        # Adding images
        self.add_image()  # TODO 后续要接入后台自动获取图片

    def add_image(self):
        for url in IMAGE_URL:
            image = AsyncImage(source=url, fit_mode="fill")
            self.add_widget(image)

    def update_images_from_server(self, *args):
        try:
            # 示例：假设从服务器获取图片URL列表
            response = requests.get('https://example.com/api/get_images')
            image_urls = response.json()  # 假设返回一个包含图片URL的列表

            # 清空旧的图片
            self.carousel.clear_widgets()

            # 添加新的图片到轮播
            for url in image_urls:
                image = Image(source=url, allow_stretch=True)
                self.carousel.add_widget(image)

            print("Images updated from server")

        except Exception as e:
            print(f"Failed to update images from server: {e}")


class CameraModule(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.camera = Camera(resolution=(1920, 1080), play=True)
        self.add_widget(self.camera)

        self.camera = Camera(resolution=(1920, 1080), play=True, index=1)
        self.add_widget(self.camera)


class LoginScreen(BoxLayout):
    """该类是用来创建登录注册组件的展示的"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class IndexScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Create the main layout (vertical BoxLayout)
        main_layout = BoxLayout(orientation='vertical', padding=[10, 15, 10, 5], spacing=10)

        # Create and add the carousel widget to the main layout
        carousel_widget = CarouselWidget()
        main_layout.add_widget(carousel_widget)

        # Add two CameraModule instances to the camera layout
        # camera_module = CameraModule(spacing=10)
        # main_layout.add_widget(camera_module)

        login_screen = LoginScreen(spacing=10)
        main_layout.add_widget(login_screen)

        self.add_widget(main_layout)
