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

from pages.index_page.index import IndexScreen
from pages.task_list_page.task_page import TaskListPage
from settings.settings_proj import INDEX_KV_PATH, LOGIN_KV_PATH, TASK_KV_PATH
from pages.login_page.login_page import LoginWidget
from utils.user_widget import BaseMDNavigationItem, MyPopup


# conda install -c conda-forge libstdcxx-ng
# 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
class RubbishApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.default_page = None
        self.screen_manager = ScreenManager()
        self.is_login = None
        self.login_user = None  # 记录登录的用户
        self.sessionid = None

    def on_switch_tabs(
            self,
            bar: MDNavigationBar,
            item: MDNavigationItem,
            item_icon: str,
            item_text: str,
    ):
        if MDApp.get_running_app().is_login and item_text == "Login":
            MyPopup(title='', content=Label(text='Login Successfully')).open()
            self.root.get_ids().screen_manager.current = "Index"
        else:
            self.root.get_ids().screen_manager.current = item_text
    def build(self):
        # 创建ScreenManager
        self.load_kv(INDEX_KV_PATH)
        self.load_kv(LOGIN_KV_PATH)
        self.load_kv(TASK_KV_PATH)
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
        manager_screen_obj = MDScreenManager(
                IndexScreen(
                    name="Index",
                    image_size="1024",
                ),
                LoginWidget(
                    name="Login",
                    image_size="800",
                ),
                TaskListPage(
                    name="Task",
                    image_size="800",
                ),
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
                BaseMDNavigationItem(
                    icon="console-network",
                    text="Task",
                ),
                on_switch_tabs=self.on_switch_tabs,
                id="bar_manager"
            ),
            orientation="vertical",
            md_bg_color=self.theme_cls.backgroundColor,
        )
        return objects


if __name__ == '__main__':
    RubbishApp().run()