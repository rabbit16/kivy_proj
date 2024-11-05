from kivy.app import App
from kivy.graphics import Color, Rectangle
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout


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
        Clock.schedule_once(self.dismiss, 1.5)  # 3 seconds auto dismiss


