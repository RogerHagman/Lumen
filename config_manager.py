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

        #Using the ConfigManager to grab a value from JSON
        brightness_levels = self.get_setting("brightness_levels", {})
        # Returns the default value if nothing specified
        default_brightness = self.get_setting("default_brightness")
        return brightness_levels.get(label, default_brightness) 
    
    def get_transition_time(self, label="SHORT"):
        transition_times = self.get_setting("transition_times", {})
        
        # Defaults  to return None if not found.
        return transition_times.get(label, 0) 