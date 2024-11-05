from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.camera import Camera
from kivy.graphics.texture import Texture
from kivy.core.image import Image as CoreImage
import io


class CameraApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')

        # Create a Camera widget
        self.camera = Camera(play=True)
        self.camera.resolution = (640, 480)  # Set the resolution

        # Add the Camera widget to the layout
        self.layout.add_widget(self.camera)

        # Create a button to capture the image
        capture_button = Button(text="Capture")
        capture_button.bind(on_press=self.capture)

        # Add the button to the layout
        self.layout.add_widget(capture_button)

        return self.layout

    def capture(self, instance):
        # Get texture from the camera and convert to image
        texture = self.camera.texture

        # Save the current frame as image
        if texture:
            # Create a buffer to store the image data

            data = io.BytesIO()
            image = CoreImage(texture)
            image.save(data, fmt='png')
            data.seek(0)

            # Save the data to a file (for example, 'captured.png')
            with open('captured.png', 'wb') as f:
                f.write(data.read())
            print("Image Captured and saved to captured.png")


if __name__ == '__main__':
    CameraApp().run()
