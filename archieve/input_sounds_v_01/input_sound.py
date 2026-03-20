import pygame
import random
import time
import os
from pynput import keyboard, mouse

pygame.init()
pygame.mixer.init()

def load_sounds(folder):
    sounds = []
    for file in os.listdir(folder):
        if file.endswith(".wav"):
            sounds.append(pygame.mixer.Sound(os.path.join(folder, file)))
    return sounds

typing_sounds = load_sounds("typing")
mouse_click_sounds = load_sounds("mouse")

space_sound = pygame.mixer.Sound("special/space.wav")
enter_sound = pygame.mixer.Sound("special/enter.wav")
backspace_sound = pygame.mixer.Sound("special/backspace.wav")

last_key_time = time.time()

def play_sound(sound):
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
        sound.set_volume(random.uniform(0.6,0.9))

    sound.play()

def on_key_press(key):

    try:
        if key == keyboard.Key.space:
            play_sound(space_sound)

        elif key == keyboard.Key.enter:
            play_sound(enter_sound)

        elif key == keyboard.Key.backspace:
            play_sound(backspace_sound)

        else:
            play_typing()

    except:
        play_typing()

def on_click(x, y, button, pressed):

    if not pressed:
        return

    if button == mouse.Button.left:
        play_sound(random.choice(mouse_click_sounds))

    if button == mouse.Button.right:
        play_sound(random.choice(mouse_click_sounds))

def on_scroll(x, y, dx, dy):

    try:
        scroll = pygame.mixer.Sound("mouse/scroll.wav")
        play_sound(scroll)
    except:
        pass

keyboard_listener = keyboard.Listener(on_press=on_key_press)
mouse_listener = mouse.Listener(
    on_click=on_click,
    on_scroll=on_scroll
)

keyboard_listener.start()
mouse_listener.start()

print("Ultra realistic input sound system running")

keyboard_listener.join()
mouse_listener.join()