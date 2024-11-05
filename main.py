# -*- coding: utf-8 -*-
# @Time    : 2024/9/24 09:40
# @Author  : rabbit
# @File    : main.py
# @Software: PyCharm
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from pages.index_page.index import IndexScreen
from settings.settings_proj import INDEX_KV_PATH, LOGIN_KV_PATH
from pages.login_page.login_page import LoginWidget


# conda install -c conda-forge libstdcxx-ng
# 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
class RubbishApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.default_page = None
        self.screen_manager = ScreenManager()
        self.login_user = None  # 记录登录的用户
        self.is_login = False  # 记录登录状态
        self.sessionid = None
    def build(self):
        # 创建ScreenManager
        self.load_kv(INDEX_KV_PATH)
        self.load_kv(LOGIN_KV_PATH)
        pages = {
            "Index": IndexScreen(),
            "Login": LoginWidget(),
        }
        for item, page in pages.items():
            self.default_page = page
            screen = Screen(name=item)
            screen.add_widget(self.default_page)
            self.screen_manager.add_widget(screen)

        return self.screen_manager


if __name__ == '__main__':
    RubbishApp().run()