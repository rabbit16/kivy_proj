import logging

import requests
from kivy.app import App
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.fitimage import FitImage
from kivymd.uix.navigationbar import MDNavigationItem, MDNavigationItemIcon, MDNavigationItemLabel
from kivymd.uix.screen import MDScreen


class MyPopup(Popup):
    """
    popup = MyPopup(title='',content=Label(text='Hello world'))
        popup.open()
    """
    def __init__(self, **kwargs):
        super(MyPopup, self).__init__(**kwargs)
        self.title = kwargs.get('title', '')
        self.content = kwargs.get('content', Label(text='Hello world'))
        self.size_hint = kwargs.get('size_hint', (None, None))
        self.size = kwargs.get('size', (130, 100))
        # self.title_color = "green"
        # Set the position to be centered horizontally and close to the top
        self.pos_hint = {'center_x': 0.5, 'top': 1}  # Center horizontally, top aligned
    def open(self, *args, **kwargs):
        super(MyPopup, self).open(*args, **kwargs)
        Clock.schedule_once(self.dismiss, 2)  # 3 seconds auto dismiss

class BaseMDNavigationItem(MDNavigationItem):
    icon = StringProperty()
    text = StringProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_widget(MDNavigationItemIcon(icon=self.icon))
        self.add_widget(MDNavigationItemLabel(text=self.text))

class BaseScreen(MDScreen):
    image_size = StringProperty()
    dragging = True
    start_size = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


def request_post(url, json_data, headers=None):
    try:
        r = requests.post(url, json=json_data, headers=headers)
        return r
    except Exception as e:
        logging.error(e)
        return {}

def request_get(url, headers=None):
    try:
        r = requests.get(url, headers=headers)
        return r
    except Exception as e:
        logging.error(e)