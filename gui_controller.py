import tkinter as tk
from tkinter import ttk
from phue import Bridge
from hue_controller import HueController

class PowerControlFrame(ttk.Frame):
    """
    A tkinter Frame Container Widget enabling controls for toggling 
    lights on and off.

    Attributes:
    - is_on (bool): A flag indicating if the lights is currently on 
                    or off.
    - canvas (tk.Canvas): A canvas displaying a visual representation 
                          of the light's state.

    Methods:
    - toggle_lights(event=None): Toggles the state of the light between 
                                 on and off.
    """
    
    # CONSTANTS

    CANVAS_WIDTH = 80
    CANVAS_HEIGHT = 80
    # Dynamicly splitting the canvas in half to center the text 
    # helps with responsiveness.
    TOGGLE_TEXT_X = CANVAS_WIDTH // 2
    TOGGLE_TEXT_Y = CANVAS_HEIGHT // 2

    def __init__(self, parent, controller: HueController):
        """
        Initialize the PowerControlFrame.

        This frame provides controls for toggling the state of the
        lights (on/off). It uses a canvas displaying a button, 
        showing the current state of the light, 
        visually represented as a green rectangle for ON that 
        alternates to a red color for OFF. When clicked, 
        the state of the light is toggled.

        Parameters:
        - parent: The parent widget.
        - controller (HueController): The controller responsible for 
                                      managing the lights 
                                      (This is where an instance of the
                                      ConfigManager and the Bridge 
                                      can be accessed).

        Attributes:
        - controller (HueController): An instance of the HueController
                                      to manage the lights.
        - is_on (bool): Flag indicating lights ON(True) or OFF(False).
        - light_switch_label (ttk.Label): A label displaying the text 
                                          "Light Switch".
        - canvas (tk.Canvas): The canvas displaying the 
                              visual representation of 
                              the light's state.
        - toggle_button: A rectangle displayed on the canvas acting as
                         a toggle button for Turning lights ON/OFF.
        - toggle_text: Text in the canvas displaying the current state
                       of the light ("ON" or "OFF").
        """
        super().__init__(parent)

        # Singleton instance of the hue controller
        self.controller = controller

        # Boolean flag to keep track of ON/OFF status for lights
        self.is_on = False  

        self.light_switch_label = \
            ttk.Label(self, text="Light Switch", justify='center')

        self.light_switch_label.grid(
            row=0, column=0, columnspan=2, pady=5, padx=0)

        self.canvas = tk.Canvas(self, width=self.CANVAS_WIDTH, 
                                height=self.CANVAS_HEIGHT, 
                                bg="black",
                                highlightthickness=1)
        
        # ON/OFF Toggle button
        self.toggle_button = \
            self.toggle_button = self.canvas.create_rectangle(5, 5, 75, 75, 
                                                              fill="red", 
                                                              outline="ivory", 
                                                              width=3, 
                                                              tags="toggle")
        
        # Add text to the middle of the ON/OFF rectangle
        self.toggle_text = self.canvas.create_text(self.TOGGLE_TEXT_X, 
                                                   self.TOGGLE_TEXT_Y, 
                                                   text="OFF", 
                                                   fill="ivory",
                                                   font=("Arial", 9, "bold"),
                                                   tags="toggle_text")
        
        self.canvas.grid(row=1, column=0, columnspan=2)
        
        # Binding mouse click to the toggle button
        self.canvas.tag_bind("toggle", "<Button-1>", self.toggle_lights)

    def toggle_lights(self, event=None):
        """
        Toggle the state of the lights and update the 
        visual representation.

        If the lights are currently turned on, this method will toggle
        them off, and vice versa. The visual representation on the 
        canvas will be updated to reflect the active state 
        of the lights. When the lights are on, the toggle button is
        colored green with the a text that says "ON", When off it will
        instead be a red color with a label that reads "OFF".

        Parameters:
        - event: The event that triggered the method. Default is None,
          which is an acceptable state allowed by the TKinter library.

        Attributes Modified:
        - is_on (bool): Flag indicating the state of the lights. 
                        This method manipulates that value.
        - toggle_button: The color fill state of the toggle button 
                         on the canvas will be updated based on the
                         state of the lights.
        - toggle_text: The text displayed in the canvas will be updated
                       to "ON" or "OFF" based on the state of the 
                       lights.
        """

        if self.is_on:
            self.controller._turn_off_lights_group(0)
            self.canvas.itemconfig(self.toggle_button, fill="red")
            self.canvas.itemconfig(self.toggle_text, text="OFF")
            self.is_on = False
        else:
            self.controller._turn_on_lights_group(0)
            self.canvas.itemconfig(self.toggle_button, fill="green")
            self.canvas.itemconfig(self.toggle_text, text="ON")
            self.is_on = True


class ColorControlFrame(ttk.Frame):
    """
    A tkinter Frame Container Widget for selecting and setting the
    color of lights.
   
    Attributes:
    - colors (list): A list of available colors.
    - color_var (tk.StringVar): A tkinter variable storing the selected 
                                color.
    - lamp_canvas (tk.Canvas): A visual representation of the current 
                               light color.

    Methods:
    - set_color(): Updates the light color based on user selection.
    """
    def __init__(self, parent, controller: HueController):
        """
        Initialize the ColorControlFrame widget.

        This frame contains a dropdown menu to select a color, 
        a button to apply the selected color to the lights,
        and a visual representation of a lamp in the form of a
        filled circle which reflects the currently selected color.

        Parameters:

        - parent: The parent widget for this frame.
        - controller: An instance of the HueController 
                      which manages the interaction 
                      with the Philips Hue lights.

        Attributes:
        - controller (HueController): 
                        Singleton instance of the HueController.
        - colors (list): List of available colors for the lights.
        - color_var (tk.StringVar): Holds the current selected color 
                                    from the dropdown.
        - color_dropdown (ttk.Combobox): Dropdown menu for color 
                                         selection.
        - color_button (ttk.Button): A Button to apply the selected 
                                     color.
        - lamp_canvas (tk.Canvas): Canvas to display a visual 
                                   representation of a lamp.
        - lamp_representation: The visual representation of the lamp
                               on the canvas.
        """
        super().__init__(parent)

        # Singleton instance of the hue controller
        self.controller = controller

        self.colors = ['RED', 'GREEN', 'BLUE', 'YELLOW', 'WHITE']
        self.color_var = tk.StringVar()
        self.color_dropdown = ttk.Combobox(self, 
                                           values=self.colors, 
                                           textvariable=self.color_var)
        self.color_dropdown.set('WHITE')
        
        # CTA (Call To Action). Pressing This button executes the current 
        # state of the dropdown menu.
        self.color_button = \
            ttk.Button(self, text="Change Color", command=self.set_color)

        # Lamp representation using a Canvas with a circle shape
        self.lamp_canvas = tk.Canvas(self, width=50, height=50, 
                                     bg="black", highlightthickness=0)
        
        # Color selection will also update the color of the lamp representation
        self.lamp_representation = \
            self.lamp_canvas.create_oval(10, 10, 40, 40, fill="WHITE")

        # Grid layout to arrange the diffrent elements of the Widget
        self.color_dropdown.grid(row=0, column=0, 
                                 padx=5, pady=10, 
                                 sticky=tk.W, columnspan=2)

        self.color_button.grid(row=1, column=0, 
                               padx=5, pady=10, 
                               sticky=tk.W)
        
        self.lamp_canvas.grid(row=1, column=1, 
                              padx=0, pady=10, 
                              sticky=tk.W)

    def set_color(self):
        """
        Apply selected color to the lights and update the lamp 
        representation.

        This method retrieves the currently selected color from a 
        dropdown menu, updates the visual representation of the lamp 
        with the selected color, and finaly uses the HueController 
        to change the color of the actual Philips Hue lights.

        Attributes Modified:
        - lamp_representation: The fill color is updated to the 
                               currently selected color and acts
                               as an abstaction of the real world
                               state of the hui lamps.
        """
        color = self.color_var.get()
        self.lamp_canvas.itemconfig(self.lamp_representation, fill=color)
        self.controller._set_light_settings(0, color=color)


class BrightnessControlFrame(ttk.Frame):
    """
    A tkinter Frame Container Widget for adjusting light 
    brightness.

    Attributes:
    - brightness_slider (tk.Scale): A slider to adjust the brightness 
                                    level.

    Methods:
    - set_brightness(event): Updates the light brightness based on the 
                             slider's currently read value.
    """
    
    def __init__(self, parent, controller: HueController):
        """
        Initializes the BrightnessControlFrame widget.

        Args:
            parent: The parent widget.
            controller (HueController): Singleton instance controlling
                                        the Hue lights.

        Attributes:
            controller (HueController): 
                                Hue light controller.
            brightness_slider_label (ttk.Label): 
                                Label for the brightness slider.
            brightness_slider (tk.Scale): 
                                Slider to control the light brightness.
        """
        super().__init__(parent)

        # Singleton instance of the hue controller
        self.controller = controller

        # Slider Label preferences
        self.brightness_slider_label = \
            ttk.Label(self, text="Brightness", justify='center')
        self.brightness_slider_label.grid(
            row=0, column=0, columnspan=2, pady=5, padx=0)

        # Slider with a custom style using tk.Scale
        self.brightness_slider = tk.Scale(self, 
                                          from_=0, 
                                          to_=254, 
                                          orient=tk.HORIZONTAL, 
                                          command=self.set_brightness,
                                          troughcolor='black',
                                          sliderrelief='solid',
                                          bg='yellow')
        
        self.brightness_slider.set(150)  # Neutral Initial setting
        self.brightness_slider.grid(row=1, column=0, columnspan=2, pady=10)

    def set_brightness(self, event):
        """
        Adjusts the light brightness based on the slider's value.

        The method determines the brightness label that corresponds to
        the current slider value using thresholds from a 
        configuration file(JSON). It then communicates with the 
        HueController in order to apply the selected brightness setting
        to the lamp(s).

        Args:
            event: Event data captured from the slider's value change.
        """
        brightness_value = int(self.brightness_slider.get())
        brightness_levels = \
            self.controller.config.get_setting("brightness_levels")
        
        label = "NEUTRAL" # Default label

        # Loops through all the brightness levels (stored in config.json)
        # And sets brightness to the nearest label using the threshold.
        for level, threshold in sorted(brightness_levels.items(),
                                       key=lambda item: item[1], reverse=True):
            # TODO In a future update this logic might be made legacy and
            # Brightness instead set directly without the aid of thresholds.
            if brightness_value >= threshold:
                label = level
                break
        
        
        self.controller._set_light_settings(0, brightness=label)


class HueControllerGUI(tk.Tk):
    """
    The main GUI applet providing a user friendly experience by 
    extending the HueController.

    Attributes:
    - power_frame (PowerControlFrame): 
                A Frame of controls for light toggling.
    - color_frame (ColorControlFrame): 
                A Frame for selecting and setting light color.
    - brightness_frame (BrightnessControlFrame): 
                A Frame dedicated to adjusting the light brightness.
    """
    def __init__(self, controller: HueController):
        """
        Initializes the HueControllerGUI main application window.

        Args:
            controller (HueController): Singleton instance controlling 
                                        the Hue lights.

        Attributes:
            power_frame (PowerControlFrame): 
                A Frame of controls for lights toggling.
            color_frame (ColorControlFrame): 
                A Frame for selecting and setting light color.
            brightness_frame (BrightnessControlFrame): 
                A Frame dedicated to adjusting the light brightness.
        """
        super().__init__()
        style = ttk.Style()
        style.configure('TFrame', background='black')
        style.configure('TLabel', background='black', foreground='ivory')
        self.configure(bg="black")
        self.power_frame = PowerControlFrame(self, controller)
        self.color_frame = ColorControlFrame(self, controller)
        self.brightness_frame = BrightnessControlFrame(self, controller)

        self.power_frame.pack(pady=10)
        self.color_frame.pack(pady=10)
        self.brightness_frame.pack(pady=10)

if __name__ == "__main__":
    """
    Execution starting point for the HueControllerGUI application.
    Initializes a HueController and launches the main GUI applet.
    """
    controller = HueController()
    gui_app = HueControllerGUI(controller)
    gui_app.mainloop()