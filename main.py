from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import Screen
from kivymd.uix.button import MDRoundFlatButton
from kivy.lang import Builder
from kivymd.uix.dialog import MDDialog
from navigation import navigation_helper
from client import Client
import json
from kivymd.uix.navigationdrawer import MDNavigationDrawerItem
import requests
from requests import HTTPError
from plyer import notification
from kivy.clock import Clock
from functools import partial
from kivymd.utils import asynckivy
from kivy.factory import Factory
from turn_on_values import turn_on_values_helper
from kivymd.uix.list import TwoLineIconListItem, ImageLeftWidget, MDList


class WateringSystem(MDApp):
    def refresh_callback(self):
        def refresh_callback(interval):
            self.screen.ids.info_box.clear_widgets()
            try:
                response = requests.get(f"http://{self.HOST}:{self.PORT}/")
                response.raise_for_status()
            except HTTPError as http_err:
                self.screen.ids.info_box.add_widget(MDLabel(text=f"HTTP error occurred: {http_err}", halign="center",font_style= "H5"))
            except Exception as err:
                self.screen.ids.info_box.add_widget(MDLabel(text=f"Other error occurred: {err}", halign="center",font_style= "H5"))
            else:           
                sensor_data = response.json()
                list = self.generate_sensor_list(sensor_data)
                self.screen.ids.info_box.add_widget(list)
            self.screen.ids.refresh_layout.refresh_done()
            self.tick = 0
        Clock.schedule_once(refresh_callback, 1)

    def submit(self,sm,host,port):
        # close_button = MDRoundFlatButton(text="Close", pos_hint={"center_x":0.7, "center_y":0.5}, on_release=self.close)
        # self.dialog = MDDialog(title="Entered information", text=text_field.text, size_hint=(0.7,1), buttons=[close_button])
        self.HOST = host.text
        self.PORT = port.text
        disconnect_button = MDRoundFlatButton(text="D", pos_hint={"center_x":0.7, "center_y":0.5}, on_release=self.close)
        notification.notify(title="Hi", message="Bye")
        sm.current = "home"
        # self.dialog.open()

    def sensor_submit(self,sm, moisture, temperature, humidity, air_quality, light):
        data = {
            "moisture": int(moisture.text) if moisture.text != "" else 0,
            "temperature": int(temperature.text) if temperature.text != "" else 0,
            "humidity": int(humidity.text) if humidity.text != "" else 0,
            "air_quality": float(air_quality.text) if air_quality.text != "" else 0,
            "light": int(light.text) if light.text != "" else 0
        }
        requests.post(f"http://{self.HOST}:{self.PORT}/", json=data)
        sm.current = "home"

    

    def sensor_data(self, sm, widget):
        widget.clear_widgets()
        try:
            response = requests.get(f"http://{self.HOST}:{self.PORT}/")
            response.raise_for_status()
        except HTTPError as http_err:
            widget.add_widget(MDLabel(text=f"HTTP error occurred: {http_err}", halign="center",font_style= "H5"))
        except Exception as err:
            widget.add_widget(MDLabel(text=f"Other error occurred: {err}", halign="center",font_style= "H5"))
        else:           
            sensor_data = response.json()
            list = self.generate_sensor_list(sensor_data)
            widget.add_widget(list)

        sm.current = "info"

        # self.client.send("Get data")
        # while True:
        #     message = self.client.receive()
        #     data = json.loads(message)
        #     for prop in data:
        #         string = prop.capitalize() + " level " + str(data[prop])
        #         self.root.ids.info_box.add_widget(MDLabel(text=string, halign="center",font_style= "H5"))            

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.theme_style_switch_animation = True

        self.screen = Builder.load_string(navigation_helper)
        # nav = Builder.load_string(navigation_helper)
        # self.screen.add_widget(nav)
        
        return self.screen
    
    def on_start(self):
        self.HOST = "192.168.2.236"
        self.PORT = 9999
    
    def toggle_mode(self,icon):
        if self.theme_cls.theme_style == "Dark":
            icon.icon = "moon-waning-crescent"
            self.theme_cls.theme_style = "Light"
        else:
            icon.icon = "white-balance-sunny"
            self.theme_cls.theme_style = "Dark"
    
    def close(self,obj):
        self.dialog.dismiss()

    def show_login(self):
        self.screen.add_widget(self.button)
        self.screen.add_widget(self.username)

    def get_turn_on_values(self, sm, moisture, temperature, humidity, air_quality, light):
        try:
            response = requests.get(f"http://{self.HOST}:{self.PORT}/turn-on-values")
            response.raise_for_status()
        except HTTPError:
            notification.notify(title="HTTP Error", message=f"A HTTP error occurred when trying to get the sensor's turn on values")
        except Exception:
            notification.notify(title="Error", message=f"An error occurred when trying got get the sensor's turn on values")
        else:           
            turn_on_values = response.json()
            moisture.text = str(turn_on_values["moisture"])
            temperature.text = str(turn_on_values["temperature"])
            humidity.text = str(turn_on_values["humidity"])
            air_quality.text = str(turn_on_values["air_quality"])
            light.text = str(turn_on_values["light"])

        sm.current = "sensor"

    def generate_sensor_list(self, data):
        list = MDList()
        for prop in data:
            text = prop.capitalize().replace("_", " ")
            list_item = TwoLineIconListItem(
                ImageLeftWidget(source=f"{text}.png"),
                text=text,
                secondary_text= str(data[prop])
                )
            # list_item.add_widget(MDRoundFlatButton(text="Details"))
            list.add_widget(list_item)
        return list
    


WateringSystem().run()
