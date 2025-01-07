import os
import sys

import requests
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import StringProperty, BooleanProperty
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
from pages.index_page.index import LabelChina
from settings.settings_proj import HTTP_URL
from utils.user_widget import MyPopup, request_get, request_post


# ICON 图标大全 https://github.com/kivymd/KivyMD/blob/master/kivymd/icon_definitions.py


# Builder.load_file('task_page.kv')
# url = f'{HTTP_URL}/task_update/?employee_number={MDApp.get_running_app().login_user}'  # 替换为实际的URL
class MyBoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        self.not_deal = None
        self.deal = None
        super(MyBoxLayout, self).__init__(**kwargs)

        # 设置中文字体
        font_path = 'static/fonts/DroidSansFallback.ttf'  # 替换为实际的字体文件路径
        self.my_font = fm.FontProperties(fname=font_path, size=15)

        # 初始数据
        self.labels = ['待办工单', '结束工单']
        self.sizes = [1, 1]  # 初始各类别的大小
        self.colors = ['red', 'yellowgreen']  # 各类别的颜色

        # 创建图形
        self.fig, self.ax = plt.subplots()
        self.patches, texts, autotexts = self.ax.pie(self.sizes, labels=self.labels, colors=self.colors,
                                                     autopct=lambda pct: self.make_label(pct, self.sizes), startangle=0,
                                                     textprops={'fontproperties': self.my_font})
        self.ax.axis('equal')  # 确保饼图是圆的

        # 将matplotlib图形放入Kivy
        canvas = FigureCanvasKivyAgg(self.fig)
        self.add_widget(canvas)

        # 每隔60秒更新一次数据
        # Clock.schedule_interval(self.update_pie_chart, 1)

    def update_pie_chart(self, dt):
        # 请求新数据
        if MDApp.get_running_app().is_login is None and MDApp.get_running_app().screen_manager != "Task":
            return True
        try:
            response = request_get(f"{HTTP_URL}/task_update/?employee_number=0")
            data = response.json()
            if data and data["data"]['待办工单'] != self.not_deal and data["data"]['结束工单'] != self.deal:
                print("更新了工单数量")
                new_sizes = [data["data"]['待办工单'], data["data"]['结束工单']]
                self.not_deal = new_sizes[0]
                self.deal = new_sizes[1]
                # 更新饼图的数据
                for i, size in enumerate(new_sizes):
                    self.patches[i].set_radius(size)
                    self.sizes[i] = size

                # 重新计算和更新autotexts
                self.ax.clear()  # 清除现有图像
                self.patches, texts, autotexts = self.ax.pie(self.sizes, labels=self.labels, colors=self.colors,
                                                             autopct=lambda pct: self.make_label(pct, self.sizes),
                                                             startangle=0, textprops={'fontproperties': self.my_font})
                self.ax.axis('equal')  # 确保饼图是圆的
                self.fig.canvas.draw()  # 重新绘制
            return True

        except requests.exceptions.RequestException as e:
            print(f"HTTP请求失败: {e}")

    # 制作标签，带有个数
    def make_label(self, pct, allvals):
        absolute = int(round(pct / 100. * sum(allvals)))
        return "{:d}".format(absolute)


class OwnMDModalDatePicker(MDModalDatePicker):
    def __init__(self, **kwargs):
        self.item = kwargs['item']
        del kwargs['item']
        super().__init__(**kwargs)

    def on_ok(self, *args) -> bool:
        if self.min_date is None:
            self.min_date = datetime.datetime.now().strftime("%Y-%m-%d")
            self.max_date = datetime.datetime.now().strftime("%Y-%m-%d")
            min_date = self.min_date
            max_date = self.max_date
        else:
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
        Clock.schedule_once(lambda dt: request_post(
            url=f"{HTTP_URL}/task_update/",
            json_data={
                "task_id": self.id,
                "update_fields": {
                    "status": 1,
                    "update_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }

            }
        ), .5)
        Clock.schedule_once(lambda dt: self.parent.parent.parent.parent.ids.task_view.update_task(), 1)




class RV(RecycleView):
    def __init__(self, **kwargs):
        self.id = "task_view"
        super(RV, self).__init__(**kwargs)
        # Sample data with ID, image source, and description
        self.is_init = False
        # Clock.schedule_interval(lambda dt: self.update_task(), 1)

    def update_task(self):
        MyPopup(title='', content=LabelChina(text='开始更新任务界面!')).open()
        if MDApp.get_running_app().screen_manager != "Task":
            return True
        self.parent.parent.ids.pic_view.update_pie_chart(None)
        r = request_get(
            url=f"{HTTP_URL}/task_info/?employee_number={MDApp.get_running_app().login_user}"
        )
        result = r.json()
        tmp = []
        self.data = tmp
        pic_source = [f"static/tmp_pic/{i['pic_url'].split('/')[-1]}" for i in result]
        flag = 0
        for task in result:
            image_url = task["pic_url"]  # pic url path
            if image_url.split("/")[-1] in pic_source:
                # continue
                pass
            else:
                if os.path.exists(f"./static/tmp_pic/{image_url.split('/')[-1]}") and self.is_init == True and False:
                    pass
                else:
                    flag = 1
                    r = request_get(f"{HTTP_URL}/static/pic_rubbish/{image_url.split('/')[-1]}")
                    with open(f"./static/tmp_pic/{image_url.split('/')[-1]}", 'wb') as f:
                        f.write(r.content)
                tmp.append({
                    "id": str(task["id"]),
                    "image_source": f"static/tmp_pic/{image_url.split('/')[-1]}",
                    "description": task["name"]
                })
        self.data = tmp


class TaskListPage(GestureBox):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.add_tasks()

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
