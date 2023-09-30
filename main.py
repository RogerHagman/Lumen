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

        
        xy = self.config.get_color_coordinates("BLUE")
        settings = {
            # 'xy' color coordinates between 0 and 1
            'xy': xy,
            # 'bri' brightness between 0 and 255
            'bri': self.config.get_setting("brightness", 254), 
            # Transition time in milliseconds
            'transitiontime': self.config.get_setting("transition_time", 50)
        }
        self.bridge.set_group(0, settings)
        time.sleep(10)
        self.bridge.set_group(0, {'transitiontime': 50, 'on': False})


if __name__ == "__main__":
    controller = HueController()
    controller.control_lights()