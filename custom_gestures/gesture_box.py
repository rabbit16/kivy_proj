# -*- coding: utf-8 -*-
# @Time    : 2024/9/27 17:31
# @Author  : rabbit
# @File    : gesture_bx.py
# @Software: PyCharm
from kivy.gesture import GestureDatabase
from kivy.uix.boxlayout import BoxLayout
from kivy.gesture import Gesture
from kivy_garden.navigationdrawer import NavigationDrawer as ND

from utils.user_widget import BaseScreen

gesture_strings = {
    'top_to_bottom_line': "eNprYJnKz84ABj082ZlllXrpqcUlpUWpU3rY3aGsyVM0G6fUTtHoYS3PTCnJmOLuoAbVwZaRmpmeUQIUqb0AEeGHao8vKMpPKU0GSbF+2JTz0oWnh724pCg/O7V4SuyUDIYeXqjpwWBBhB1sBfmZeSUgRRpAVTxQVQEgQYQixoop7vvreL8YJggz9DBWAjmPrpnz1Lt2lSZlCELUZIi4728OkvmtXXkgQ9R9/0O2lpDPRhY45R94zgpj/fUBp/xtiAFky99yuZmftlIZp/w1Gf7F/0UqyZa/mPmwxkPwFM3kz5Zejy29HoVT/sCUvG3MbbeoK19avi4n06gBJD/Tl3cSn1MDfeUzD130e7KUAShvP8tiKveu/wmo8oE63Z1vT4Dld33m+rZTZAHN5I/xn3YIzlpBtvzJi53H6nPOoMjbg/03Byx/fsfNvS/VOXDKXzR+fnS32iRUeXD46YPlL4sc57iovgRVHpxDBcDyV/pms62ehpo/7Nvn2t9d9sIBJH/ddsIViz1+qPLdL5IOKEWA5W8UbVr8uhiYPlJ7eIqTi1JT8xDlhLtDxQFw6ePuIP4fBJ62AYudig14xCAFGC+KmEMDmIEi5gammVHEgsGWMaKIhe0H2fEPRSyuHlMseT7YMShiaQqY5uUgiV2AihUaIMQeQMWKNiDc/AEqViqAKVaOTewDXKySH+wsICMAixiSOgWo3qoLCDGIs9wdquvhfkOInUeIOUD11iDZEQBVV3MAixiSvQlQvbUBWMTWI+yAi2HRW2cAFUstTUrs4SzJz0ktSsxLTp3ibr9zJgjM6mHJS8wF1nwMU0qT9ABdUKkI",
    "left_to_right_line": "eNprYJnazs4ABj082ZlllXrpqcUlpUWpU3rY3aGsyVM0G6fUTtHoYS3PTCnJmOLu0OAB0cGWkZqZnlECFFH+DwIPevih2uMLivJTSpNBUuzu9h3pcx/0sBeXFOVnpxZPiZ2SwdDDCzU9GCyIsIOtID8zrwSkSAOoigeqKgAkiFDEWDHFff+TwmWWi7yDehgrgZxWjSAx5WcMpUkZghA1GSLu+x+Hzb+W8DE9QxSH/INNTdHc79+RLX9b0fTGr0cBIPlGK6aa8N8N1JW/HhSx+2+4E9ny59b0ieu5RYHkq6anHpVQorP83mfz4/9argDJp+7x233hIwN95TeodBzd3AoKX/vgnBhVmSOkydvPvM68q/lnAki+ZEpoQdmtBurKb9eabOO8qAIkX1PwZQnfegbS5Pd1ZtQs/PkBp/xRLe2lTHc6cMofny+bquTPg1P+NP9i7i17FHDKn2vQ2OSuaQKSb1I7+fqy4wFU+UuFW9kkndlw+v/ya6H7R3e9Acln5udU7uNGM/8a41rNKv4ClPhN7eEpTi5KTc1DlBPuDkqQEszdoWQBmNEGLHZUsIhpYBHTA7MYUcSssahzasAUC8QiFucAE9sAF0tmwBTLVoCJHYCLFU6AiT2AixUHQMVKGeBiZQYwMQW4WAVcnQFcrNIBU6zqAKZYdQI0DJDEahywiD2A6bUHl/cgsVoFmDokMQMs6hywiAVgEWvAIrYAU6yOAdN9dfvB0ijhUg83TwAh9gEWzh/gYtA6DSXsGxKwiMHj/AJCrAOL2AR0sdTSpMQezpL8nNSixLzk1Cnu9jtngsCsHpa8xFxgjcswpTRJDwAHf6/G",
    "right_to_left_line": "eNprYJnazs4ABj082ZlllXrpqcUlpUWpU3"
                          "rY3aGsyVM0G6fUTtHoYS3PTCnJmOLu0KQB0cGWkZq"
                          "ZnlECFHFpgIjwQ7XHFxTlp5Qmg6RYX17z/PjYpIe9uKQoPzu1e"
                          "ErslAyGHl6o6cFgQYQdbAX5mXklIEUaQFU8UFUBIEGEIsaKKe72D6s5o/1vS/"
                          "QwVgI5y7dbBAXmPyhNyhCEqMkQcbd/YLZ34qdH0zJE3e0X+1vf2MqSgCp/l9lrDU93CUh+wapCzX"
                          "AtB9Lkb2xv9BfhZAHJz/KQ1tzC94A0+asLX+mqdU0AyU+2DmHYeRLNfZd/va7vfuQAku/PfHCj0pcBVf7Cmnc"
                          "qYRPngOQbA4LaWg4eIE3+lK+o/Ka7C4Dy+5WfX/9trYBm/rE+78C3L8DyuYWzlOecRJPfa3+tf"
                          "cUWsHzj+4lucbMaSJNfm"
                          "/W9zZNLACTf8SciP+IBA2nyc+4vmJeV44BLfv80W1AEJoDke5r2MF9jOkCa/MaSC88vRswAyU"
                          "9g6T+jOQk1/vbvjUr4832dBNnyx2s1"
                          "C7esEyBb/tSkA5MX6XTglL/gdMRfavUinPKXbTRCUhwZyJa/dm8/a6vPM5zyNxZ+OH/4nh9O+Z"
                          "vpYTPsbV/jlL+9vf3jxpjDIPmJxw9Oy1AB5r/U"
                          "Hp7i5KLU1DxEOeHu0LEDXPq4O5QqgBltwGKnYwVMTAAhVgAVK/mAEGOAiV2Ai7XDzCs5gBDjgIkt"
                          "gIu1wewomQAXa70AE0uAi7V8gImB3ccIFquAi"
                          "THA1TV3QMWKEfY2wcXy/4MAWAzm5mJ/uFjDA5gYIgzqN8DEEHbUL"
                          "cAUqwG7mdHdoQgRLtUKUHVFD+BilQWYYhULMMXKPmARE8AUgwYRiljRBkyxQizmFWCxN98BUywPix05DzD"
                          "Fsg/AxBDpIDsBFi5IYrCwL0LEUdYCmLoNCDG4W2BpI7U0KbGHsyQ/J7UoMS8"
                          "5FVhr7ZwJArN6WPISc4E1LsOU0iQ9AJcSoG0="

}
# 存储手势数据
gestures = GestureDatabase()
for name, gesture_string in gesture_strings.items():
    gesture = gestures.str_to_gesture(gesture_string)
    gesture.name = name
    gestures.add_gesture(gesture)


class GestureBox(BaseScreen):
    def __init__(self, **kwargs):
        for name in gesture_strings:
            self.register_event_type('on_{}'.format(name))
        super(GestureBox, self).__init__(**kwargs)

    def on_left_to_right_line(self):
        pass

    def on_right_to_left_line(self):
        pass

    def on_bottom_to_top_line(self):
        pass

    def on_top_to_bottom_line(self):
        pass

    def on_touch_down(self, touch):
        touch.ud["gesture_path"] = [(touch.x, touch.y)]  # 这就是创建了一个字典
        super(GestureBox, self).on_touch_down(touch)  # 这里是调用父类的touch方法。

    def on_touch_move(self, touch):
        touch.ud["gesture_path"].append((touch.x, touch.y))
        super(GestureBox, self).on_touch_move(touch)

    def on_touch_up(self, touch):
        if "gesture_path" in touch.ud:
            gesture = Gesture()
            gesture.add_stroke(touch.ud["gesture_path"])
            gesture.normalize()
            match = gestures.find(gesture, minscore=0.8)
            if match:
                print({"{} happened".format(match[1].name)})
                self.dispatch('on_{}'.format(match[1].name))
        super(GestureBox, self).on_touch_up(touch)