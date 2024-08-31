from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivy.lang import Builder
from navigation import navigation_helper
import requests
from requests import HTTPError
from plyer import notification
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image


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
                self.generate_sensor_list(sensor_data)
            self.screen.ids.refresh_layout.refresh_done()
            self.tick = 0
        Clock.schedule_once(refresh_callback, 1)

    def submit(self,sm,host,port):
        self.HOST = host.text
        self.PORT = port.text
        sm.current = "home"

    def sensor_submit(self,sm, moisture, temperature, humidity, air_quality, light):
        data = {
            "moisture": float(moisture.text) if moisture.text != "" else 0,
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
            self.generate_sensor_list(sensor_data)

        sm.current = "info"         

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.theme_style_switch_animation = True

        self.screen = Builder.load_string(navigation_helper)
        
        return self.screen
    
    def on_start(self):
        self.HOST = "192.168.112.15"
        self.PORT = 9999
    
    def toggle_mode(self,icon):
        if self.theme_cls.theme_style == "Dark":
            icon.icon = "moon-waning-crescent"
            self.theme_cls.theme_style = "Light"
        else:
            icon.icon = "white-balance-sunny"
            self.theme_cls.theme_style = "Dark"

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
        for prop in data:
            text = prop.replace("_", " ").capitalize()
            image = Image(source=f"{text}.png")
            self.screen.ids.info_box.add_widget(image)
            info = BoxLayout(orientation="vertical")
            info.add_widget(MDLabel(text=text, font_style="H6", halign="center"))
            info.add_widget(MDLabel(text=format(data[prop], ".2f"), font_style="Subtitle1", halign="center"))
            self.screen.ids.info_box.add_widget(info)

    def manual_control(self, acctuator, state):
        if(acctuator == "fan" and state == "on"):
            requests.post(f"http://{self.HOST}:{self.PORT}/fan/on")
        elif(acctuator == "fan" and state == "off"):
            requests.post(f"http://{self.HOST}:{self.PORT}/fan/off")
        elif(acctuator == "pump" and state == "on"):
            requests.post(f"http://{self.HOST}:{self.PORT}/pump/on")
        elif(acctuator == "pump" and state == "off"):
            requests.post(f"http://{self.HOST}:{self.PORT}/pump/off")
        elif(acctuator == "light" and state == "on"):
            requests.post(f"http://{self.HOST}:{self.PORT}/light/on")
        elif(acctuator == "light" and state == "off"):
            requests.post(f"http://{self.HOST}:{self.PORT}/light/off")


WateringSystem().run()
