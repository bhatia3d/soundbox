from pynput import keyboard, mouse
import pygame

# Initialize sound system
pygame.init()
pygame.mixer.init()

# Load sounds
type_sound = pygame.mixer.Sound("typing.wav")
click_sound = pygame.mixer.Sound("click.wav")

# Keyboard event
def on_key_press(key):
    type_sound.play()

# Mouse event
def on_click(x, y, button, pressed):
    if pressed:
        click_sound.play()

# Start listeners
keyboard_listener = keyboard.Listener(on_press=on_key_press)
mouse_listener = mouse.Listener(on_click=on_click)

keyboard_listener.start()
mouse_listener.start()

print("Listening for keyboard and mouse input...")

keyboard_listener.join()
mouse_listener.join()
