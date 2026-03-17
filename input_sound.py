import pygame
import random
import time
import os
import sys
import tkinter as tk
from pynput import keyboard, mouse

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def load_sounds(folder):
    sounds = []
    for file in os.listdir(folder):
        if file.endswith(".wav"):
            sounds.append(pygame.mixer.Sound(os.path.join(folder, file)))
    return sounds

pygame.init()
pygame.mixer.init()

typing_sounds = load_sounds(resource_path("typing"))
left_click_sound = pygame.mixer.Sound(resource_path("mouse/left.wav"))
right_click_sound = pygame.mixer.Sound(resource_path("mouse/right.wav"))
space_sound = pygame.mixer.Sound(resource_path("special/space.wav"))
enter_sound = pygame.mixer.Sound(resource_path("special/enter.wav"))
backspace_sound = pygame.mixer.Sound(resource_path("special/backspace.wav"))
scroll_sound = pygame.mixer.Sound(resource_path("mouse/scroll/scroll.wav"))
last_key_time = time.time()
keyboard_listener = None
mouse_listener = None

def play_sound(sound, fixed=False):
    if fixed:
        sound.set_volume(1.0)
    else:
        volume = random.uniform(0.6, 1.0)
        sound.set_volume(volume)
    sound.play()

def play_typing():
    global last_key_time
    now = time.time()
    interval = now - last_key_time
    last_key_time = now
    sound = random.choice(typing_sounds)
    if interval < 0.07:
        sound.set_volume(1.0)
    else:
        sound.set_volume(random.uniform(0.6, 0.9))
    sound.play()

def on_key_press(key):
    try:
        if key == keyboard.Key.space:
            play_sound(space_sound, True)
        elif key == keyboard.Key.enter:
            play_sound(enter_sound, True)
        elif key == keyboard.Key.backspace:
            play_sound(backspace_sound, True)
        else:
            play_typing()
    except:
        play_typing()

def on_click(x, y, button, pressed):
    if not pressed:
        return
    if button == mouse.Button.left:
        play_sound(left_click_sound, True)
    elif button == mouse.Button.right:
        play_sound(right_click_sound, True)

def on_scroll(x, y, dx, dy):
    play_sound(scroll_sound, True)

# START FUNCTION
def start_listening():
    global keyboard_listener, mouse_listener
    if keyboard_listener is None:
        keyboard_listener = keyboard.Listener(on_press=on_key_press)
        mouse_listener = mouse.Listener(
            on_click=on_click,
            on_scroll=on_scroll
        )
        keyboard_listener.start()
        mouse_listener.start()
        status_label.config(text="Status: Running")

# STOP FUNCTION
def stop_listening():
    global keyboard_listener, mouse_listener
    if keyboard_listener:
        keyboard_listener.stop()
        keyboard_listener = None
    if mouse_listener:
        mouse_listener.stop()
        mouse_listener = None
    status_label.config(text="Status: Stopped")

# GUI
root = tk.Tk()
root.title("Input Sound System")
root.geometry("250x150")
start_button = tk.Button(root, text="Start", width=15, command=start_listening)
start_button.pack(pady=10)
stop_button = tk.Button(root, text="Stop", width=15, command=stop_listening)
stop_button.pack(pady=10)
status_label = tk.Label(root, text="Status: Stopped")
status_label.pack(pady=10)
root.mainloop()