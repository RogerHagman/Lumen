import tkinter as tk
from tkinter import ttk
from phue import Bridge
from hue_controller import HueController

class PowerControlFrame(ttk.Frame):
    """Frame containing controls for turning lights on and off."""
    
    # CONSTANTS

    CANVAS_WIDTH = 80
    CANVAS_HEIGHT = 80
    # Dynamicly splitting the canvas in half to center the text 
    # helps with responsiveness.
    TOGGLE_TEXT_X = CANVAS_WIDTH // 2
    TOGGLE_TEXT_Y = CANVAS_HEIGHT // 2

    def __init__(self, parent, controller: HueController):
        super().__init__(parent)
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
        """Toggle lights based on the current status."""

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
    """Frame containing controls for setting light color."""
    def __init__(self, parent, controller: HueController):
        super().__init__(parent)
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
        color = self.color_var.get()
        self.lamp_canvas.itemconfig(self.lamp_representation, fill=color)
        self.controller._set_light_settings(0, color=color)


class BrightnessControlFrame(ttk.Frame):
    """Frame containing controls for adjusting light brightness."""
    
    def __init__(self, parent, controller: HueController):
        super().__init__(parent)
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
        brightness_value = int(self.brightness_slider.get())
        brightness_levels = self.controller.config.get_setting("brightness_levels")
        
        label = "NEUTRAL" # Default label

        # Loops through all the brightness levels (stored in config.json)
        # And sets brightness to the nearest label using the threshold.
        for level, threshold in sorted(brightness_levels.items(), 
                                       key=lambda item: item[1], reverse=True):
            if brightness_value >= threshold:
                label = level
                break
        
        
        self.controller._set_light_settings(0, brightness=label)


class HueControllerGUI(tk.Tk):
    def __init__(self, controller: HueController):
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
    controller = HueController()
    gui_app = HueControllerGUI(controller)
    gui_app.mainloop()