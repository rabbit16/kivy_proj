# -*- coding: utf-8 -*-
# @Time    : 2024/9/24 09:40
# @Author  : rabbit
# @File    : main.py
# @Software: PyCharm
from kivy.app import App
from kivy.core.window import Window
from kivy.properties import BooleanProperty
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.navigationbar import MDNavigationBar, MDNavigationItem
from kivymd.uix.screenmanager import MDScreenManager

from pages.devices_list_page.device_page import DeviceListPage
from pages.index_page.index import IndexScreen
from pages.task_list_page.task_page import TaskListPage
from settings.settings_proj import INDEX_KV_PATH, LOGIN_KV_PATH, TASK_KV_PATH, DEVICE_KV_PATH, IS_MOBILE
from pages.login_page.login_page import LoginWidget
from queue import Queue
import os

from utils.user_widget import BaseMDNavigationItem, MyPopup


# conda install -c conda-forge libstdcxx-ng
# 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
# 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
class RubbishApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.default_page = None
        self.screen_manager = None
        self.is_login = None
        self.login_user = None  # 记录登录的用户
        self.sessionid = None
        self.is_setting = True if IS_MOBILE else None
        # FIXME 这里来一个断点续传
        self.queue_camera_0 = Queue()
        self.queue_camera_1 = Queue()
        self.queue_pic = Queue()  # 用于分析人物指标统计的
        self.queue_pic2 = Queue()  # 用于分析小包垃圾的
        self.camera_0_is_sending = False  # 控制第一个摄像头的发送情况
        self.camera_1_is_sending = False  # 控制第二个摄像头的发送情况

    def on_switch_tabs(
            self,
            bar: MDNavigationBar,
            item: MDNavigationItem,
            item_icon: str,
            item_text: str,
    ):
        if MDApp.get_running_app().is_login and item_text == "Login":
            MyPopup(title='', content=Label(text='Login Successfully')).open()
            if IS_MOBILE:
                self.root.get_ids().screen_manager.current = "Task"
            else:
                self.root.get_ids().screen_manager.current = "Index"
        else:
            self.root.get_ids().screen_manager.current = item_text
            self.screen_manager = item_text

    def build(self):
        # 创建ScreenManager
        self.load_kv(INDEX_KV_PATH)
        self.load_kv(LOGIN_KV_PATH)
        self.load_kv(TASK_KV_PATH)
        self.load_kv(DEVICE_KV_PATH)
        # pages = {
        #     "Index": IndexScreen(),
        #     "Login": LoginWidget(),
        # }
        # for item, page in pages.items():
        #     self.default_page = page
        #     screen = Screen(name=item)
        #     screen.add_widget(self.default_page)
        #     self.screen_manager.add_widget(screen)
        # Window.fullscreen=0#不设置全屏
        # Window.size=(330,550)#窗口大小
        if IS_MOBILE:
            manager_screen_obj = MDScreenManager(
                # IndexScreen(
                #     name="Index",
                # ),
                LoginWidget(
                    name="Login",
                ),
                TaskListPage(
                    name="Task",
                ),
                DeviceListPage(
                    name="Device",

                ),
                id="screen_manager",
            )
            objects = MDBoxLayout(
                manager_screen_obj
                ,
                MDNavigationBar(
                    # BaseMDNavigationItem(
                    #     icon="home",
                    #     text="Index",
                    #     active=True,
                    # ),
                    BaseMDNavigationItem(
                        icon="login",
                        text="Login",
                    ),
                    BaseMDNavigationItem(
                        icon="console-network",
                        text="Task",
                    ),
                    BaseMDNavigationItem(
                        icon="power",
                        text="Device",
                    ),
                    on_switch_tabs=self.on_switch_tabs,
                    id="bar_manager"
                ),
                orientation="vertical",
                md_bg_color=self.theme_cls.backgroundColor,
            )
        else:
            manager_screen_obj = MDScreenManager(
                IndexScreen(
                    name="Index",
                ),
                LoginWidget(
                    name="Login",
                ),
                # TaskListPage(
                #     name="Task",
                # ),
                # DeviceListPage(
                #     name="Device",
                #
                # ),
                id="screen_manager",
            )
            objects = MDBoxLayout(
                manager_screen_obj
                ,
                MDNavigationBar(
                    BaseMDNavigationItem(
                        icon="home",
                        text="Index",
                        active=True,
                    ),
                    BaseMDNavigationItem(
                        icon="login",
                        text="Login",
                    ),
                    # BaseMDNavigationItem(
                    #     icon="console-network",
                    #     text="Task",
                    # ),
                    # BaseMDNavigationItem(
                    #     icon="power",
                    #     text="Device",
                    # ),
                    on_switch_tabs=self.on_switch_tabs,
                    id="bar_manager"
                ),
                orientation="vertical",
                md_bg_color=self.theme_cls.backgroundColor,
            )
        return objects


if __name__ == '__main__':
    RubbishApp().run()
