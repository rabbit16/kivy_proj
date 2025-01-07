from kivy.clock import Clock
from kivy.compat import clock
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy_garden.matplotlib import FigureCanvasKivyAgg
from kivymd.app import MDApp
from kivymd.font_definitions import theme_font_styles
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.list import MDListItem, MDListItemLeadingIcon, MDListItemHeadlineText, MDListItemSupportingText
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.pickers import MDModalDatePicker
from kivymd.uix.segmentedbutton import MDSegmentedButton, MDSegmentButtonIcon
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import datetime
from kivy import __version__ as kv__version__
from kivymd import __version__
from materialyoucolor import __version__ as mc__version__
from custom_gestures.gesture_box import GestureBox
from settings.settings_proj import HTTP_URL, FONT_NAME
from utils.user_widget import request_get


# ICON 图标大全 https://github.com/kivymd/KivyMD/blob/master/kivymd/icon_definitions.py


# Builder.load_file('device_page.kv')
class LabelChinaDevice(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_name = FONT_NAME
        self.text_size
        self.halign = 'center'  # 左对齐
        self.valign = 'center'  # 垂直居中（根据需求调整）
        self.color = "black"
class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    ''' Adds selection and focus behavior to the view. '''
class SelectableLabelDevice(RecycleDataViewBehavior, BoxLayout):
    id = StringProperty("")  # Unique ID for display
    device_name = StringProperty("")  # Image source/path
    device_addr = StringProperty("")  # Task description
    device_status = StringProperty("")  # Task description
    def on_button_click(self):
        ''' Handle button click event. '''
        print(f'Button clicked for item ID: {self.id} | Description: {self.device_name} | Status: {self.device_status}')

class RVDevice(RecycleView):
    def __init__(self, **kwargs):
        super(RVDevice, self).__init__(**kwargs)
        # Sample data with ID, image source, and description
        Clock.schedule_interval(lambda dt: self.add_tasks(), 6)
        # self.add_tasks()
    def add_tasks(self, *args):
        # print(MDApp.get_running_app().login_user)
        if MDApp.get_running_app().screen_manager != "Device":
            return True
        if MDApp.get_running_app().login_user is None or MDApp.get_running_app().is_setting is None:
            pass
        else:
            r = request_get(f"{HTTP_URL}/devices/?employee_number={MDApp.get_running_app().login_user}")
            info = r.json()

            # 清空现有 widgets
            # 将任务分批执行
            tmp_list = []
            for info_item in info:
                tmp_list.append({
                    "id": str(info_item['id']),
                    "device_name": str(info_item['children']),
                    "device_addr": info_item['device_addr'],
                    "device_status": str(info_item['status']),
                })
            tmp_list.insert(0, {
                    "id": "id",
                    "device_name": "device_name",
                    "device_addr": "device_addr",
                    "device_status": "device_status",
                })
            self.data = tmp_list

class SingleImageItem(BoxLayout):
    def __init__(self, id_image, url, describe, **kwargs):
        super(SingleImageItem, self).__init__(**kwargs)
        self.image_source = url
        self.describe = describe
        self.orientation = 'horizontal'
        self.size_hint = (1, None)
        self.label_id = Label(text=str(id_image), size_hint=(.1, None))
        self.add_widget(self.label_id)
        self.image_show = Image(source=self.image_source, size_hint=(.2, None))
        self.add_widget(self.image_show)
        self.label = Label(text=self.describe, size_hint=(.5, None))
        self.add_widget(self.label)
        self.button = Button(text="deal", size_hint=(.4, None))
        self.add_widget(self.button)


class DeviceListPage(GestureBox):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.add_tasks()
        # Clock.schedule_interval(self.add_tasks, 3)

    def menu_callback(self, text_item):
        self.ids.drop_text.text = text_item

    def add_tasks(self, *args):
        print(MDApp.get_running_app().login_user)
        if MDApp.get_running_app().login_user is None or MDApp.get_running_app().is_setting is None:
            pass
        else:
            r = request_get(f"{HTTP_URL}/devices/?employee_number={MDApp.get_running_app().login_user}")
            info = r.json()

            # 清空现有 widgets
            self.ids.main_scroll.clear_widgets()

            # 将任务分批执行
            for info_item in info:
                Clock.schedule_once(lambda dt: self.add_device_item(info_item), 0)

    def add_device_item(self, info_item):
        self.ids.main_scroll.add_widget(
            MDListItem(
                MDListItemLeadingIcon(
                    icon="check" if info_item["status"] == 0 else "close",
                ),
                MDListItemHeadlineText(
                    text=info_item["device_addr"],
                    theme_font_name="Custom",
                    font_name="static/fonts/DroidSansFallback.ttf"
                ),
                MDListItemSupportingText(
                    text=str(info_item["children"]),
                ),
                pos_hint={"center_x": .5, "center_y": .5},
            )
        )


class DeviceListApp(MDApp):
    def build(self):
        return DeviceListPage()


if __name__ == '__main__':
    DeviceListApp().run()
