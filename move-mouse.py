#!/usr/bin/env python3
"""Move the mouse left and right repeatedly.

Usage:
    python3 move-mouse.py [--distance 200] [--delay 0.5] [--count 0]

    --distance  pixels to move left/right (default 200)
    --delay     seconds between each move (default 0.5)
    --count     number of left-right cycles, 0 = forever (default 0)

Defaults can also come from environment variables or a .env file:
    MOVE_DISTANCE, MOVE_DELAY, MOVE_COUNT (CLI args take precedence).

Stop with ESC, right-click, or Ctrl+C.
"""
import argparse
import sys
import threading

import config

try:
    import pyautogui
except ImportError:
    sys.exit("pyautogui not installed. Run: uv pip install pyautogui")

try:
    from pynput import keyboard, mouse
except ImportError:
    sys.exit("pynput not installed. Run: uv pip install pynput")


# set when ESC is pressed or the right mouse button is clicked
stop_event = threading.Event()


def _on_key(key):
    if key == keyboard.Key.esc:
        stop_event.set()


def _on_click(_x, _y, button, pressed):
    if pressed and button == mouse.Button.right:
        stop_event.set()


def main():
    parser = argparse.ArgumentParser(description="Move mouse left and right")
    parser.add_argument("--distance", type=int, default=config.DEFAULT_DISTANCE, help="pixels to move")
    parser.add_argument("--delay", type=float, default=config.DEFAULT_DELAY, help="seconds between moves")
    parser.add_argument("--count", type=int, default=config.DEFAULT_COUNT, help="cycles, 0 = forever")
    parser.add_argument("--center", action="store_true", help="move cursor to screen center before starting")
    args = parser.parse_args()

    # let the mouse move freely; disable the corner fail-safe
    pyautogui.FAILSAFE = False

    # optionally start from the middle of the monitor
    if args.center:
        width, height = pyautogui.size()
        pyautogui.moveTo(width // 2, height // 2, duration=0.2)
        print(f"Centered cursor at {width // 2}, {height // 2}")

    # listen for ESC / right-click in the background (daemon so we can exit)
    key_listener = keyboard.Listener(on_press=_on_key)
    key_listener.daemon = True
    key_listener.start()
    click_listener = mouse.Listener(on_click=_on_click)
    click_listener.daemon = True
    click_listener.start()

    cycles = 0
    print("Moving mouse left/right. Press ESC, right-click, or Ctrl+C to stop.")
    try:
        while not stop_event.is_set() and (args.count == 0 or cycles < args.count):
            pyautogui.moveRel(args.distance, 0, duration=0.2)   # right
            if stop_event.wait(args.delay):
                break
            pyautogui.moveRel(-args.distance, 0, duration=0.2)  # left
            if stop_event.wait(args.delay):
                break
            cycles += 1
    except KeyboardInterrupt:
        pass
    print("\nStopped.")


if __name__ == "__main__":
    main()
