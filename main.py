import os
import random
import threading
import time
import tkinter

import customtkinter
import pynput

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("500x300")
        self.resizable(0, 0)
        self.title("Auto Clicker")
        self.iconphoto(False, tkinter.PhotoImage(file=os.path.join("icon", "icon.png")))

        self.left_hotkey = customtkinter.StringVar(self, "'x'")
        self.right_hotkey = customtkinter.StringVar(self, "Key.ctrl_l")

        self.delay = customtkinter.StringVar(self, f"Click Delay (0.06)")
        self.offset = customtkinter.StringVar(self, f"Random Offset (0.04)")

        self.top_frame = customtkinter.CTkFrame(master=self)
        self.top_frame.place(anchor="n", x=250, y=10, w=480, h=120)

        self.delay_label = customtkinter.CTkLabel(master=self.top_frame, textvariable=self.delay)
        self.delay_label.place(anchor="n", x=240, y=10)

        self.delay_slider = customtkinter.CTkSlider(master=self.top_frame, from_=10, to=1000,
                                                    command=lambda delay: self.delay.set(f"Click Delay ({round(delay / 1000, 2)})"))
        self.delay_slider.place(anchor="n", x=240, y=40, w=460, h=20)
        self.delay_slider.set(60)

        self.offset_label = customtkinter.CTkLabel(master=self.top_frame, textvariable=self.offset)
        self.offset_label.place(anchor="n", x=240, y=60)

        self.offset_slider = customtkinter.CTkSlider(master=self.top_frame, from_=0, to=1000,
                                                     command=lambda delay: self.offset.set(f"Random Offset ({round(delay / 1000, 2)})"))
        self.offset_slider.place(anchor="n", x=240, y=90, w=460, h=20)
        self.offset_slider.set(40)

        self.middle_frame_top = customtkinter.CTkFrame(master=self)
        self.middle_frame_top.place(anchor="center", x=250, y=175, w=480, h=70)

        self.left_main_button_frame = customtkinter.CTkFrame(master=self.middle_frame_top)
        self.left_main_button_frame.place(anchor="w", x=10, y=35, w=225, h=50)

        self.left_button_frame = customtkinter.CTkFrame(master=self.left_main_button_frame)
        self.left_button_frame.place(anchor="w", x=10, y=25, w=97.5, h=30)

        self.left_button_label = customtkinter.CTkLabel(master=self.left_button_frame, text="Hotkey")
        self.left_button_label.place(anchor="center", x=48.75, y=15, w=97.5, h=20)

        self.left_hotkey_entry = customtkinter.CTkEntry(master=self.left_main_button_frame, textvariable=self.left_hotkey)
        self.left_hotkey_entry.place(anchor="e", x=215, y=25, w=97.5, h=30)

        self.left_main_mouse_button_frame = customtkinter.CTkFrame(master=self.middle_frame_top)
        self.left_main_mouse_button_frame.place(anchor="e", x=470, y=35, w=225, h=50)

        self.left_mouse_button_frame = customtkinter.CTkFrame(master=self.left_main_mouse_button_frame)
        self.left_mouse_button_frame.place(anchor="w", x=10, y=25, w=97.5, h=30)

        self.left_mouse_button_label = customtkinter.CTkLabel(master=self.left_mouse_button_frame, text="Mouse Button")
        self.left_mouse_button_label.place(anchor="center", x=48.75, y=15, w=97.5, h=20)

        self.left_button_label = customtkinter.CTkLabel(master=self.left_main_mouse_button_frame, text="Left")
        self.left_button_label.place(anchor="e", x=215, y=25, w=97.5, h=30)

        self.middle_frame_bottom = customtkinter.CTkFrame(master=self)
        self.middle_frame_bottom.place(anchor="center", x=250, y=255, w=480, h=70)

        self.right_main_button_frame = customtkinter.CTkFrame(master=self.middle_frame_bottom)
        self.right_main_button_frame.place(anchor="w", x=10, y=35, w=225, h=50)

        self.right_button_frame = customtkinter.CTkFrame(master=self.right_main_button_frame)
        self.right_button_frame.place(anchor="w", x=10, y=25, w=97.5, h=30)

        self.right_button_label = customtkinter.CTkLabel(master=self.right_button_frame, text="Hotkey")
        self.right_button_label.place(anchor="center", x=48.75, y=15, w=97.5, h=20)

        self.right_hotkey_entry = customtkinter.CTkEntry(master=self.right_main_button_frame, textvariable=self.right_hotkey)
        self.right_hotkey_entry.place(anchor="e", x=215, y=25, w=97.5, h=30)

        self.right_main_mouse_button_frame = customtkinter.CTkFrame(master=self.middle_frame_bottom)
        self.right_main_mouse_button_frame.place(anchor="e", x=470, y=35, w=225, h=50)

        self.right_mouse_button_frame = customtkinter.CTkFrame(master=self.right_main_mouse_button_frame)
        self.right_mouse_button_frame.place(anchor="w", x=10, y=25, w=97.5, h=30)

        self.right_mouse_button_label = customtkinter.CTkLabel(master=self.right_mouse_button_frame, text="Mouse Button")
        self.right_mouse_button_label.place(anchor="center", x=48.75, y=15, w=97.5, h=20)

        self.right_button_label = customtkinter.CTkLabel(master=self.right_main_mouse_button_frame, text="right")
        self.right_button_label.place(anchor="e", x=215, y=25, w=97.5, h=30)


class Clicker:
    def __init__(self):
        self.left_clicking = False
        self.right_clicking = False

    def calculate_delay(self, app):
        subtracted_offset = round((float(app.delay.get()[13:-1]) - float(app.offset.get()[15:-1])) * 1000)
        added_offset = round((float(app.delay.get()[13:-1]) + float(app.offset.get()[15:-1])) * 1000)

        if subtracted_offset < 0.01:
            subtracted_offset = 0.01

        if subtracted_offset > added_offset:
            subtracted_offset = added_offset

        return random.randint(round(subtracted_offset), round(added_offset)) / 1000

    def clicker(self, app):
        while True:
            if self.left_clicking:
                pynput.mouse.Controller().click(pynput.mouse.Button.left)

            if self.right_clicking:
                pynput.mouse.Controller().click(pynput.mouse.Button.right)

            time.sleep(self.calculate_delay(app))

    def on_press(self, key, app):
        if str(key) == app.left_hotkey.get():
            self.left_clicking = not self.left_clicking

        if str(key) == app.right_hotkey.get():
            self.right_clicking = not self.right_clicking


def keyboard_listener(app, clicker):
    with pynput.keyboard.Listener(on_press=lambda key: clicker.on_press(key, app)) as keyboard_listener:
        keyboard_listener.join()


def main():
    app = App()
    clicker = Clicker()
    clicker_thread = threading.Thread(target=clicker.clicker, args=(app,))
    clicker_thread.daemon = True
    clicker_thread.start()
    keyboard_listener_thread = threading.Thread(target=keyboard_listener, args=(app, clicker))
    keyboard_listener_thread.daemon = True
    keyboard_listener_thread.start()
    app.mainloop()


if __name__ == "__main__":
    main()
