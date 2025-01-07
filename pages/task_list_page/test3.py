from kivy.app import App
from kivy.lang import Builder
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.properties import BooleanProperty, StringProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior

# Load Kivy Language string
Builder.load_string('''
<SelectableLabel>:
    orientation: 'horizontal'
    Label:
        text: str(root.id)  # Display ID
        size_hint_x: 0.1  # 10% for ID
    Image:
        source: root.image_source  # Path to the image
        size_hint_x: 0.2  # 20% for image
        allow_stretch: True
        keep_ratio: True
    Label:
        text: root.description  # Task description
        size_hint_x: 0.5  # 50% for description
    Button:
        text: 'Click Me'
        size_hint_x: 0.2  # 20% for button
        on_release: root.on_button_click()

<RV>:
    viewclass: 'SelectableLabel'
    SelectableRecycleBoxLayout:
        default_size: None, dp(56)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'
        multiselect: True
        touch_multiselect: True
''')


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    ''' Adds selection and focus behavior to the view. '''


class SelectableLabel(RecycleDataViewBehavior, BoxLayout):
    ''' Add selection support to the Label, Image, and Button '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)
    id = StringProperty("")  # Unique ID for display
    image_source = StringProperty("")  # Image source/path
    description = StringProperty("")  # Task description

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index

        # Set the attributes, ensuring they are strings
        self.id = str(data['id']) if 'id' in data else 'N/A'
        self.image_source = str(data['image_source']) if 'image_source' in data else ''
        self.description = str(data['description']) if 'description' in data else ''

        return super(SelectableLabel, self).refresh_view_attrs(rv, index, data)

    def on_button_click(self):
        ''' Handle button click event. '''
        print(f'Button clicked for item ID: {self.id} | Description: {self.description}')

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        if is_selected:
            print("Selection changed to {0}".format(rv.data[index]))
        else:
            print("Selection removed for {0}".format(rv.data[index]))


class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        # Sample data with ID, image source, and description
        self.data = [
            {'id': str(i), 'image_source': 'path_to_image.png', 'description': f'Task description {i}'}
            for i in range(10)  # Reducing to 10 for demonstration
        ]


class TestApp(App):
    def build(self):
        return RV()


if __name__ == '__main__':
    TestApp().run()
