from config_manager import ConfigManager
from phue import Bridge 

import time

class HueController:
    """
    HueController controls the Philips Hue lights via the phue Bridge.

    Attributes:
    - config (ConfigManager): Instance of the ConfigManager to retrieve
      application settings.
    - bridge_ip (str): IP address of the phue Bridge.
    - bridge (Bridge): Instance of the phue Bridge to communicate with
                       the Hue lights.

    Methods:
    - _turn_on_lights_group: Turns on a group of lights with optional
                             transition time.
    - _turn_off_lights_group: Turns off a group of lights with optional
                              transition time.
    - _set_light_settings: Adjusts settings of a group of lights, 
                           including color and brightness.
    - test_lights: An example routine to demonstrate light controls.
    """
    def __init__(self):
        """
        Initializes HueController by connecting to the phue Bridge.
        """
        self.config = ConfigManager()
        self.bridge_ip = self.config.get_setting("bridge_ip")
        self.bridge = Bridge(self.bridge_ip)

        # Connects to the bridge (may need to press the link button first).
        self.bridge.connect()

    def _turn_on_lights_group(self, group_id = 0, transition_time="SHORT"):
        """
        Turns on a group of lights.

        Args:
            group_id (int, optional): 
                            The ID of the group of lights to control.
                            Defaults group is 0.
            transition_time (str, optional): 
                            The label specifying the time taken to 
                            transition Default transition label is 
                            "SHORT".
        """
        transition = self.config.get_transition_time(transition_time)
        self.bridge.set_group(group_id, 
                                {
                                  'transitiontime': transition,
                                  'on': True
                                }
                                )
    
    def _turn_off_lights_group(self, group_id, transition_time="NONE"):
        """
        Turns off a group of lights.

        Args:
            group_id (int): The ID of the group of lights to control.
            transition_time (str, optional): 
                    The label specifying the time taken to transition.
                    Defaults to "NONE".
        """
        transition = self.config.get_transition_time(transition_time)
        self.bridge.set_group(group_id, 
                                {
                                    'transitiontime': transition,
                                    'on': False
                                }
                                )

    def _set_light_settings(self,
                            group_id,
                            color="WHITE",
                            brightness="NEUTRAL",
                            transition_time="SHORT"):
        """
        Adjusts settings of a group of lights.

        Args:
            group_id (int): The ID of the group of lights to control.
            color (str, optional): 
                The label for the color to set. Defaults to "WHITE".
            brightness (str, optional): 
                The label for the brightness level to set.
                Defaults to "NEUTRAL".
            transition_time (str, optional): 
                The label specifying the time taken to transition.
                Defaults to "SHORT".
        """
        settings = {
            'xy': self.config.get_color_coordinates(color),
            'bri': self.config.get_brightness(brightness),
            'transitiontime': self.config.get_transition_time(transition_time)
        }
        self.bridge.set_group(group_id, settings)

    def test_lights(self):
        """
        A test method putting on a lightshow in three stages 
        demonstrating some of the typical controls of the 
        HueController.
        """
        self._turn_on_lights_group(0)
        self._set_light_settings(
            0, 
            color="RED", 
            brightness="VERY_BRIGHT", 
            transition_time="VERY_SHORT")
        time.sleep(2)
        self._set_light_settings(
            0, 
            color="GREEN", 
            brightness="VERY_DIM", 
            transition_time="SHORT")
        time.sleep(2)
        self._set_light_settings(
            0, 
            color="BLUE", 
            brightness="VERY_BRIGHT", 
            transition_time="VERY_SHORT")
        time.sleep(2)
        self._turn_off_lights_group(0, transition_time="SHORT")