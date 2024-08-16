from kivymd.uix.button import MDRoundFlatButton
from kivymd.uix.list import IRightBodyTouch

class Right_Button(IRightBodyTouch, MDRoundFlatButton):
    def __init__(self, **kwargs):
        # make sure we aren't overriding any important functionality
        super(Right_Button, self).__init__(**kwargs)
    pos_hint = .9 , .5
    text_color = "red"