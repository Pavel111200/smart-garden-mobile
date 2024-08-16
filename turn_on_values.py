turn_on_values_helper = """
MDScreen:
    id: sensor
    name: "sensor"
    MDBoxLayout:
        orientation: "vertical"
        size_hint: 0.7, 0.9
        pos_hint: {"center_x":0.5, "center_y":0.55}
        spacing: 20
    MDTextField:
        id: moisture
        hint_text: "Enter soil moisture in %"
        helper_text: "must be between 0 and 100"
        icon_right: "percent"
        helper_text_mode: "on_focus"
    MDTextField:
        id: temperature
        hint_text: "Enter temperature in Celsius"
        helper_text: "must be between -40 and 85"
        icon_right: "temperature-celsius"
        helper_text_mode: "on_focus"
    MDTextField:
        id: humidity
        hint_text: "Enter humidity in %"
        helper_text: "must be between 0 and 100"
        icon_right: "percent"
        helper_text_mode: "on_focus"
    MDTextField:
        id: air_quality
        hint_text: "Enter air quality"
        helper_text: "must be between 0 and 1"
        icon_right: "air-filter"
        helper_text_mode: "on_focus"
    MDTextField:
        id: light
        hint_text: "Enter light level"
        helper_text: "must be between 0 and 65535"
        icon_right: "lightbulb-on-90"
        helper_text_mode: "on_focus"
    MDRectangleFlatButton:
        text: "Submit"
        pos_hint: {"center_x":0.5, "center_y":0.1}
        on_release: app.sensor_submit(screen_manager, moisture, temperature, humidity, air_quality, light)
"""