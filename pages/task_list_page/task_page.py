from kivymd.app import MDApp

from custom_gestures.gesture_box import GestureBox


class TaskListPage(GestureBox):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class TaskListApp(MDApp):
    def build(self):
        return TaskListPage()

if __name__ == '__main__':
    TaskListApp().run()