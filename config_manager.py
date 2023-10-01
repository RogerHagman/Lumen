import json

class SingletonMeta(type):
    """A metaclass for the Singleton Pattern ensuring that only 
    one instance of a class derived from SingletonMeta can be 
    instantiated."""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class ConfigManager(metaclass=SingletonMeta):
    """
    ConfigManager handles the application's configuration by loading 
    and fetching settings from a JSON file.

    Attributes:
    - config_path (str): Path to the JSON configuration file.
    - config_data (dict): Parsed configuration data from the JSON file.

    Methods:
    - _load_config: Reads and parses the JSON configuration file.
    - get_setting: Retrieves a setting value by key from config_data.
    - get_color_coordinates: Gets coordinates for a specific color.
    - get_brightness: Fetches brightness level for a specific label.
    - get_transition_time: Retrieves transition time for a given label.
    """
    def __init__(self, config_path="config.json"):
        """
        Initializes the ConfigManager with a default or specified path
        to the configuration file.

        Args:
            config_path (str, optional):
                Path to the JSON configuration file.
                Defaults to "config.json".
        """
        self.config_path = config_path
        self.config_data = self._load_config()

    def _load_config(self):
        """
        Loads and parses the configuration JSON file.

        Returns:
            dict: Parsed configuration data.
        """
        with open(self.config_path, 'r') as config_file:
            return json.load(config_file)

    def get_setting(self, key, default=None):
        """
        Retrieves a setting's value using its key.

        Args:
            key (str): The key corresponding to the setting's value.
            default (optional): A default value to return if the key
                                isn't found.

        Returns:
            The value corresponding to the given key or the default 
            value if the key is not present.
        """
        return self.config_data.get(key, default)
    
    def get_color_coordinates(self, color_name):
        """
        Fetches coordinates of a specific color.

        Args:
            color_name (str): The name of the color.

        Returns:
            A value representing the coordinates of the color.
        """
        return self.get_setting("color_coordinates").get(color_name)

    def get_brightness(self, label="NEUTRAL"):
        """
        Retrieves the brightness level for a specific label.

        Args:
            label (str, optional): The label for the brightness level.
                                   Defaults to "NEUTRAL".

        Returns:
            int: Brightness level corresponding to the label or the
                 default brightness.
        """
        #Using the ConfigManager to grab a value from JSON
        brightness_levels = self.get_setting("brightness_levels", {})
        # Returns the default value if nothing specified
        default_brightness = self.get_setting("default_brightness")
        return brightness_levels.get(label, default_brightness) 
    
    def get_transition_time(self, label="SHORT"):
        """
        Fetches the transition time for a given label.

        Args:
            label (str, optional): The label for the transition time.
                                   Defaults to "SHORT".

        Returns:
            int: Transition time corresponding to the label or a 
            default value if not found.
        """
        transition_times = self.get_setting("transition_times", {})
        
        # Defaults to return None if not found.
        return transition_times.get(label, 0)