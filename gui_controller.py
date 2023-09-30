import tkinter as tk
from tkinter import ttk
from phue import Bridge
from hue_controller import HueController

class PowerControlFrame(ttk.Frame):
    """Frame containing controls for turning lights on and off."""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.is_on = False  # A flag to keep track of light status

        self.light_switch_label = ttk.Label(self, text="Light Switch", justify='center')
        self.light_switch_label.grid(row=0, column=0, columnspan=2, pady=5, padx=0)

        self.canvas = tk.Canvas(self, width=80, height=80, bg="black", highlightthickness=1)
        self.toggle_button = self.canvas.create_rectangle(5, 5, 75, 75, fill="red", tags="toggle")
        
        # Add text to the middle of the rectangle
        self.toggle_text = self.canvas.create_text(40, 40, text="OFF", fill="white", tags="toggle_text")
        
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
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.colors = ['RED', 'GREEN', 'BLUE', 'YELLOW']
        self.color_var = tk.StringVar()
        self.color_dropdown = ttk.Combobox(self, values=self.colors, textvariable=self.color_var)
        self.color_dropdown.set('GREEN')
        self.color_button = ttk.Button(self, text="Set Color", command=self.set_color)

        self.color_dropdown.pack(padx=5, pady=10)
        self.color_button.pack(padx=5, pady=10)

    def set_color(self):
        color = self.color_var.get()
        self.controller._set_light_settings(0, color=color)


class BrightnessControlFrame(ttk.Frame):
    """Frame containing controls for adjusting light brightness."""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.brightness_slider = ttk.Scale(self, 
                                           from_=0, 
                                           to_=254, 
                                           orient=tk.HORIZONTAL, 
                                           command=self.set_brightness)
        self.brightness_slider.set(150)  # Neutral setting
        self.brightness_slider.pack(pady=10)

    def set_brightness(self, event):
        brightness = int(self.brightness_slider.get())
        label = "NEUTRAL"
        if brightness >= 200:
            label = "VERY_BRIGHT"
        elif brightness >= 150:
            label = "BRIGHT"
        elif brightness >= 100:
            label = "DIM"
        elif brightness < 100:
            label = "VERY_DIM"
        
        self.controller._set_light_settings(0, brightness=label)


class HueControllerGUI(tk.Tk):
    def __init__(self, controller: HueController):
        super().__init__()
        style = ttk.Style()
        style.configure('TFrame', background='black')
        style.configure('TLabel', background='black', foreground='white')  # If you want labels to be styled too.
        self.controller = controller
        self.configure(bg="black")
        self.power_frame = PowerControlFrame(self, controller)
        self.color_frame = ColorControlFrame(self, controller)
        self.brightness_frame = BrightnessControlFrame(self, controller)

        self.power_frame.pack(pady=10)
        self.color_frame.pack(pady=10)
        self.brightness_frame.pack(pady=10)

if __name__ == "__main__":
    controller = HueController()
    app = HueControllerGUI(controller)
    app.mainloop()