import json
import time
from phue import Bridge

class SingletonMeta(type):
    """A metaclass for the Singleton Pattern."""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class ConfigManager(metaclass=SingletonMeta):
    def __init__(self, config_path="config.json"):
        self.config_path = config_path
        self.config_data = self._load_config()

    def _load_config(self):
        with open(self.config_path, 'r') as config_file:
            return json.load(config_file)

    def get_setting(self, key, default=None):
        return self.config_data.get(key, default)
    
    def get_color_coordinates(self, color_name):
        return self.get_setting("color_coordinates").get(color_name)

    def get_brightness(self, label="NEUTRAL"):
        brightness_levels = self.get_setting("brightness_levels", {})
        return brightness_levels.get(label, 150)
    
    def get_transition_time(self, label="SHORT"):
        transition_times = self.get_setting("transition_times", {})
        return transition_times.get(label, 0) # Default to None if not found.
    
class HueController:
    def __init__(self):
        self.config = ConfigManager()
        self.bridge_ip = self.config.get_setting("bridge_ip")
        self.bridge = Bridge(self.bridge_ip)
        self.bridge.connect()  # Ensure you've pressed the link button

    def control_lights(self):
        self.bridge.get_light_objects()

        # Turn on all lights in group
        time.sleep(10)
        self.bridge.set_group(0, 'on', True)

        settings = {
            # 'xy' color coordinates between 0 and 1
            'xy': self.config.get_color_coordinates("GREEN"),
            
            'bri': # 'bri' brightness between 0 and 255
            self.config.get_brightness("VERY_BRIGHT"),
            
            'transitiontime': # 'transitiontime' Transition time in milliseconds
            self.config.get_transition_time("VERY_SHORT")
        }
        self.bridge.set_group(0, settings)
        time.sleep(10)
        self.bridge.set_group(0, {
            'transitiontime': self.config.get_transition_time("NONE"), 
            'on': False})


if __name__ == "__main__":
    controller = HueController()
    controller.control_lights()