#!/usr/bin/env python3
"""Move the mouse left and right repeatedly.

Usage:
    python3 move-mouse.py [--distance 200] [--delay 0.5] [--count 0]

    --distance  pixels to move left/right (default 200)
    --delay     seconds between each move (default 0.5)
    --count     number of left-right cycles, 0 = forever (default 0)

Stop with ESC, right-click, or Ctrl+C.
"""
import argparse
import sys
import threading
import time

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
        return False  # stop the listener


def _on_click(x, y, button, pressed):
    if pressed and button == mouse.Button.right:
        stop_event.set()
        return False  # stop the listener


def main():
    parser = argparse.ArgumentParser(description="Move mouse left and right")
    parser.add_argument("--distance", type=int, default=200, help="pixels to move")
    parser.add_argument("--delay", type=float, default=0.5, help="seconds between moves")
    parser.add_argument("--count", type=int, default=0, help="cycles, 0 = forever")
    args = parser.parse_args()

    # let the mouse move freely; disable the corner fail-safe
    pyautogui.FAILSAFE = False

    # listen for ESC / right-click in the background
    keyboard.Listener(on_press=_on_key).start()
    mouse.Listener(on_click=_on_click).start()

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
