from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import Screen
from kivymd.uix.button import MDRectangleFlatButton
from kivy.lang import Builder
from kivymd.uix.dialog import MDDialog
from navigation import navigation_helper

data = {
    "moisture": 85,
    "temp": 26,
    "humidity": 23,
    "air_quality": 23,
    "light": 23
}

class WateringSystem(MDApp):

    def submit(self,sm,text_field):
        close_button = MDRectangleFlatButton(text="Close", pos_hint={"center_x":0.7, "center_y":0.5}, on_release=self.close)
        self.dialog = MDDialog(title="Entered information", text=text_field.text, size_hint=(0.7,1), buttons=[close_button])
        self.dialog.open()

    def sensor_submit(self,sm):
        sm.current = "home"

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Green"

        self.screen = Screen()
        nav = Builder.load_string(navigation_helper)
        self.screen.add_widget(nav)
        
        return Builder.load_string(navigation_helper)
    
    def on_start(self):
        for prop in data:
            string = prop.capitalize() + " level " + str(data[prop])
            self.root.ids.info_box.add_widget(MDLabel(text=string, halign="center",font_style="H5"))
        
    
    def close(self,obj):
        self.dialog.dismiss()

    def show_login(self):
        self.screen.add_widget(self.button)
        self.screen.add_widget(self.username)


WateringSystem().run()
