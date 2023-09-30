"""Lumen Lights ON 

- A lightweight smart home manager

"""

from gui_controller import HueControllerGUI
from hue_controller import HueController

    
if __name__ == "__main__":
    controller = HueController()
    run_app = HueControllerGUI(controller)
    run_app.mainloop()