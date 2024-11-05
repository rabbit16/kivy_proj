from kivy.app import App
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.camera import Camera
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock

class RoundedCamera(Camera):
    def __init__(self, **kwargs):
        super(RoundedCamera, self).__init__(**kwargs)

        # 使用 Kivy 的绘图指令来创建圆角矩形
        with self.canvas.before:
            # 设置颜色
            Color(1, 1, 1, 1)  # 白色
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[20])  # 20 是圆角半径

        # 在每次更新时更新矩形的位置和大小
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, instance, value):
        self.rect.pos = self.pos
        self.rect.size = self.size

class MyApp(App):
    def build(self):
        layout = FloatLayout()
        camera = RoundedCamera(index=0, play=True, size_hint=(1, 1))
        layout.add_widget(camera)
        return layout

if __name__ == '__main__':
    MyApp().run()
