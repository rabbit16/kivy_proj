from kivy.uix.label import Label
from kivy.uix.popup import Popup

from custom_gestures.gesture_box import GestureBox

# Builder.load_file('login_page.kv')

from kivy.app import App
from kivymd.app import MDApp
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Rectangle

from settings.settings_proj import HTTP_URL, IS_MOBILE
from utils.user_widget import MyPopup, request_post


class CustomTextInput(TextInput):
    def __init__(self, **kwargs):
        super(CustomTextInput, self).__init__(**kwargs)

        # Removing default background
        self.background_color = (0, 0, 0, 0)
        self.cursor_color = (0, 0, 1, 1)
        self.foreground_color =  (0, 0, 0, 1)  # 红色字体
        with self.canvas.after:
            Color(0.75, 0.75, 0.75, 1)# Black color for the line
            self.line = Rectangle(size=(self.width, 1), pos=(self.x, self.y))

        self.bind(pos=self.update_line, size=self.update_line)

    def update_line(self, *args):
        self.line.pos = (self.x, self.y)
        self.line.size = (self.width, 1)

class LoginWidget(GestureBox):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def login(self, username, password):
        # TODO 这里写登录逻辑
        headers = {
            "Cookie": MDApp.get_running_app().sessionid
        }
        MDApp.get_running_app().headers = headers
        response = request_post(
            url=HTTP_URL+"/login/",
            json_data={
                "employee_number": username,
                "password": password
            },
            headers=headers
        )
        if response.json()["errno"] == "0":
            MDApp.get_running_app().sessionid = response.headers["Set-Cookie"]
            MyPopup(title='',content=Label(text='Login Successfully')).open()
            MDApp.get_running_app().login_user = username
            MDApp.get_running_app().is_login = True
            if IS_MOBILE:
                MDApp.get_running_app().root.get_ids().screen_manager.current = 'Task'
                MDApp.get_running_app().screen_manager = "Task"
            else:
                MDApp.get_running_app().root.get_ids().screen_manager.current = 'Index'
                MDApp.get_running_app().screen_manager = "Index"
        else:
            MyPopup(title='', content=Label(text='Login failed. Please try again!')).open()
    @staticmethod
    def back_to_index():
        MDApp.get_running_app().root.current = 'Index'

class LoginPageApp(MDApp):
    def build(self):
        return LoginWidget()
if __name__ == '__main__':
    LoginPageApp().run()