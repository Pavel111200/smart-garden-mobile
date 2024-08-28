navigation_helper = """
MDScreen:
    BoxLayout:
        orientation: "vertical"
        MDTopAppBar:
            title: "Smart Garden"
            left_action_items: [["menu", lambda x: nav_drawer.set_state("toggle")]]
            specific_text_color: "#ffffff"
        Widget:
    MDNavigationLayout:   
        MDScreenManager:
            id: screen_manager
            MDScreen:
                name: "home"
                MDBoxLayout:
                    orientation: "vertical"
                    pos_hint: {"center_x": .5, "center_y": .5}
                    size_hint: 1, .75
                    FitImage:
                        source: "plant.png"
                        size_hint_x: None
                        size_hint_y: None
                        width: "300px"
                        height: "300px"
                        pos_hint: {"center_x": .5, "center_y": .5}
                    MDLabel:
                        text: "Welcome to the smart garden app"
                        halign: "center"
                        font_style: "H4"
            MDScreen:
                name: "connect"
                MDTextField:
                    id: host
                    hint_text: "Enter host"
                    pos_hint: {"center_x":0.5, "center_y":0.5}
                    helper_text: "must be between 3 and 15 charecters"
                    size_hint_x: 0.7
                    helper_text_mode: "on_focus"
                    icon_left: "server"
                MDTextField:
                    id: port
                    hint_text: "Enter port number"
                    pos_hint: {"center_x":0.5, "center_y":0.4}
                    helper_text: "must be between 3 and 5 charecters"
                    size_hint_x: 0.7
                    helper_text_mode: "on_focus"
                    icon_left: "server"
                MDRoundFlatButton:
                    text: "Submit"
                    pos_hint: {"center_x":0.5, "center_y":0.3}
                    on_press: app.submit(screen_manager, host, port)
            MDScreen:
                name: "info"
                MDScrollViewRefreshLayout:
                    id: refresh_layout
                    refresh_callback: app.refresh_callback
                    size_hint: 1, .88
                    root_layout: root
                    spinner_color: "green"
                    circle_color: "black"                   
                    # pos_hint: {"center_x": .5, "center_y": .5}
                    pos_hint_x : .5
                    GridLayout:
                        id: info_box
                        cols: 2  
                        padding: [10,10,10,10]
                        spacing: [20,10]
                        row_default_height: 100
                        # size_hint: 1, .94    
                        size_hint_y: None
                        pos_hint: {"center_x": .5, "center_y": .5}   
                        height: self.minimum_height  
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
            MDScreen:
                name: "manual"
                GridLayout:
                    size_hint: 1, .88
                    cols: 2
                    MDBoxLayout:
                        orientation: "vertical"
                        Image:
                            source: "Electric-Fan.png"
                        MDBoxLayout:
                            MDRaisedButton:
                                text: "ON"
                                text_color: "white"
                                md_bg_color: (0.3, 0.69, 0.32, 1)
                                pos_hint: {"center_x":0.5, "center_y":0.2}
                                on_release: app.manual_control("fan", "on")
                            MDRaisedButton:
                                text: "OFF"
                                text_color: "white"
                                md_bg_color: "red"
                                pos_hint: {"center_x":0.6, "center_y":0.2}
                                on_release: app.manual_control("fan", "off")
                    MDBoxLayout:
                        orientation: "vertical"
                        Image:
                            source: "Watering-can.png"
                        MDBoxLayout:
                            MDRaisedButton:
                                text: "ON"
                                text_color: "white"
                                md_bg_color: (0.3, 0.69, 0.32, 1)
                                pos_hint: {"center_x":0.4, "center_y":0.2}
                                on_release: app.manual_control("pump", "on")
                            MDRaisedButton:
                                text: "OFF"
                                text_color: "white"
                                md_bg_color: "red"
                                pos_hint: {"center_x":0.6, "center_y":0.2}
                                on_release: app.manual_control("pump", "off")
                    MDBoxLayout:
                        orientation: "vertical"
                        Image:
                            source: "Light.png"
                        MDBoxLayout:
                            MDRaisedButton:
                                text: "ON"
                                text_color: "white"
                                md_bg_color: (0.3, 0.69, 0.32, 1)
                                pos_hint: {"center_x":0.4, "center_y":0.2}
                                on_release: app.manual_control("light", "on")
                            MDRaisedButton:
                                text: "OFF"
                                text_color: "white"
                                md_bg_color: "red"
                                pos_hint: {"center_x":0.6, "center_y":0.2}
                                on_release: app.manual_control("light", "off")
        MDNavigationDrawer:
            id: nav_drawer
            radius: 0, dp(16), dp(16), 0
            MDNavigationDrawerMenu:
                MDNavigationDrawerHeader:
                    title: "Menu"
                    source: "plant_icon.png"
                MDNavigationDrawerDivider:
                MDNavigationDrawerItem:
                    text: "Home"
                    icon: "home"
                    on_release: screen_manager.current = "home"
                    icon_color: "#4caf50"
                    text_color: "#ffffff"
                    selected_color: "#ffffff"
                MDNavigationDrawerItem:
                    icon: "connection"
                    text: "Connect"
                    on_release: screen_manager.current = "connect"
                    icon_color: "#4caf50"
                    text_color: "#ffffff"
                    selected_color: "#ffffff" 
                MDNavigationDrawerDivider:
                MDNavigationDrawerItem:
                    icon: "information"
                    text: "Sensor info"
                    on_release: app.sensor_data(screen_manager, info_box)
                    icon_color: "#4caf50"
                    text_color: "#ffffff"
                    selected_color: "#ffffff"
                MDNavigationDrawerItem:
                    icon: "motion-sensor"
                    text: "Adjust sensors"
                    on_release: app.get_turn_on_values(screen_manager, moisture, temperature, humidity, air_quality, light)
                    icon_color: "#4caf50"
                    text_color: "#ffffff"
                    selected_color: "#ffffff"
                MDNavigationDrawerItem:
                    icon: "motion-sensor"
                    text: "Manual control"
                    on_release: screen_manager.current = "manual"
                    icon_color: "#4caf50"
                    text_color: "#ffffff"
                    selected_color: "#ffffff"                     
"""