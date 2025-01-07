import os
import sys

from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy_garden.matplotlib import FigureCanvasKivyAgg
from kivymd.app import MDApp
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


# ICON 图标大全 https://github.com/kivymd/KivyMD/blob/master/kivymd/icon_definitions.py


# Builder.load_file('task_page.kv')

class MyBoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(MyBoxLayout, self).__init__(**kwargs)

        # 设置中文字体
        # 你可能需要调整字体路径以适合你的系统
        font_path = 'static/fonts/DroidSansFallback.ttf'  # 替换为实际的字体文件路径
        my_font = fm.FontProperties(fname=font_path, size=15)

        # 数据
        labels = ['待办工单', '已提工单', '超时工单', '结束工单']
        sizes = [15, 30, 45, 10]  # 各类别的大小
        colors = ['red', 'yellowgreen', 'lightcoral', 'lightskyblue']  # 各类别的颜色

        # 制作标签，带有个数
        def make_label(pct, allvals):
            absolute = int(round(pct / 100. * sum(allvals)))
            return "{:d}".format(absolute)

        # 创建图形
        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, colors=colors, autopct=lambda pct: make_label(pct, sizes), startangle=0,
               textprops={'fontproperties': my_font})
        ax.legend(title="", loc="best", prop=my_font)
        ax.axis('equal')  # 确保饼图是圆的

        # 将matplotlib图形放入Kivy
        canvas = FigureCanvasKivyAgg(fig)
        self.add_widget(canvas)


class OwnMDModalDatePicker(MDModalDatePicker):
    def __init__(self, **kwargs):
        self.item = kwargs['item']
        del kwargs['item']
        super().__init__(**kwargs)

    def on_ok(self, *args) -> bool:
        min_date = self.min_date.strftime("%Y-%m-%d")
        max_date = self.max_date.strftime("%Y-%m-%d")
        print(min_date, max_date)
        self.dismiss()
        if "时间" in self.item._label.text or "至" in self.item._label.text:
            self.item._label.text = f"{min_date}至{max_date}"
        return True

    def on_cancel(self, *args) -> bool:
        self.dismiss()
        return True


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


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    ''' Adds selection and focus behavior to the view. '''


class SelectableLabel(RecycleDataViewBehavior, BoxLayout):
    id = StringProperty("")  # Unique ID for display
    image_source = StringProperty("")  # Image source/path
    description = StringProperty("")  # Task description

    def on_button_click(self):
        ''' Handle button click event. '''
        print(f'Button clicked for item ID: {self.id} | Description: {self.description}')


class TaskListPage(GestureBox):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_tasks()

    def open_menu(self, item):
        # item._label.text 获取标签的文本
        if "时间" in item._label.text or "至" in item._label.text:
            date_dialog = OwnMDModalDatePicker(mode="range", item=item)
            date_dialog.open()
        else:
            # menu_items = [
            #     {
            #         "text": f"{i}",
            #         "on_release": lambda x=f"Item {i}": self.menu_callback(x),
            #     } for i in range(5)
            # ]
            # MDDropdownMenu(caller=item, items=menu_items).open()
            pass

    def menu_callback(self, text_item):
        self.ids.drop_text.text = text_item

    def add_tasks(self):
        info = {
            "Name": [
                os.name,
                (
                    "microsoft"
                    if os.name == "nt"
                    else ("linux" if os.uname()[0] != "Darwin" else "apple")
                ),
            ],
            "Architecture": [os.uname().machine, "memory"],
            "Hostname": [os.uname().nodename, "account"],
            "Python Version": ["v" + sys.version, "language-python"],
            "Kivy Version": ["v" + kv__version__, "alpha-k-circle-outline"],
            "KivyMD Version": ["v" + __version__, "material-design"],
            "MaterialYouColor Version": ["v" + mc__version__, "invert-colors"],
            "Pillow Version": ["Unknown", "image"],
            "Working Directory": [os.getcwd(), "folder"],
            "Home Directory": [os.path.expanduser("~"), "folder-account"],
            "Environment Variables": [os.environ, "code-json"],
        }

        try:
            from PIL import __version__ as pil__version_

            info["Pillow Version"] = ["v" + pil__version_, "image"]
        except Exception:
            pass
        test = [
            SingleImageItem(1, "static/proj_img/yu.jpeg", "test"),
            SingleImageItem(2, "static/proj_img/yu.jpeg", "test"),
            SingleImageItem(3, "static/proj_img/yu.jpeg", "test"),
            SingleImageItem(4, "static/proj_img/yu.jpeg", "test"),
            SingleImageItem(5, "static/proj_img/yu.jpeg", "test"),
        ]
        for info_item in test:
            # self.ids.main_scroll.add_widget(
            #     MDListItem(
            #         MDListItemLeadingIcon(
            #             icon=info[info_item][1],
            #         ),
            #         MDListItemHeadlineText(
            #             text=info_item,
            #         ),
            #         MDListItemSupportingText(
            #             text=str(info[info_item][0]),
            #         ),
            #         pos_hint={"center_x": .5, "center_y": .5},
            #     )
            # )
            self.ids.main_scroll.add_widget(
                info_item
            )


class TaskListApp(MDApp):
    def build(self):
        return TaskListPage()


if __name__ == '__main__':
    TaskListApp().run()
