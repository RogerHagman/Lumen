from config_manager import ConfigManager
from phue import Bridge 

import time

class HueController:
    def __init__(self):
        self.config = ConfigManager()
        self.bridge_ip = self.config.get_setting("bridge_ip")
        self.bridge = Bridge(self.bridge_ip)
        self.bridge.connect()  # Ensure you've pressed the link button

    def _turn_on_lights_group(self, group_id = 0):
        self.bridge.set_group(group_id, 'on', True)
    
    def _turn_off_lights_group(self, group_id, transition_time="NONE"):
        transition = self.config.get_transition_time(transition_time)
        self.bridge.set_group(group_id, {'transitiontime': transition, 'on': False})
    
    def _set_light_settings(self, group_id, color="GREEN", brightness="NEUTRAL", transition_time="SHORT"):
        settings = {
            'xy': self.config.get_color_coordinates(color),
            'bri': self.config.get_brightness(brightness),
            'transitiontime': self.config.get_transition_time(transition_time)
        }
        self.bridge.set_group(group_id, settings)

    def control_lights(self):
        self._turn_on_lights_group(0)
        self._set_light_settings(0, color="GREEN", brightness="VERY_BRIGHT", transition_time="VERY_SHORT")
        time.sleep(10)
        self._turn_off_lights_group(0, transition_time="NONE")