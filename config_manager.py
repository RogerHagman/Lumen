import json

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