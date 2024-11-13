from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton

KV = '''
<DropDownWrapper@MDBoxLayout>:
    orientation: "horizontal"
    spacing: dp(10)
    size_hint_x: None
    width: "180dp"

    MDTextField:
        id: drop_text
        hint_text: "Select an item"
        size_hint_x: None
        width: "140dp"

    MDIconButton:
        icon: "chevron-down"
        pos_hint: {"center_y": .5, "top": 1}
        on_release: app.open_drop_item_menu(self, drop_text)

MDScreen:
    MDBoxLayout:
        orientation: "horizontal"
        spacing: dp(10)
        padding: dp(10)

        DropDownWrapper:
        DropDownWrapper:
        DropDownWrapper:
'''

class Test(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def open_drop_item_menu(self, button, text_widget):
        menu_items = [
            {
                "text": f"Item {i}",
                "on_release": lambda x=f"Item {i}": self.set_item(text_widget, x),
            } for i in range(5)
        ]
        menu = MDDropdownMenu(
            caller=button,
            items=menu_items,
            position="center",
        )
        menu.open()

    def set_item(self, text_widget, text_item):
        text_widget.text = text_item

if __name__ == "__main__":
    Test().run()
