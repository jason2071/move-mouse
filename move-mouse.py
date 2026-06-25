#!/usr/bin/env python3
"""Move the mouse left and right repeatedly.

Usage:
    python3 move_mouse.py [--distance 200] [--delay 0.5] [--count 0]

    --distance  pixels to move left/right (default 200)
    --delay     seconds between each move (default 0.5)
    --count     number of left-right cycles, 0 = forever (default 0)

Stop with Ctrl+C.
"""
import argparse
import sys
import time

try:
    import pyautogui
except ImportError:
    sys.exit("pyautogui not installed. Run: pip3 install pyautogui")


def main():
    parser = argparse.ArgumentParser(description="Move mouse left and right")
    parser.add_argument("--distance", type=int, default=200, help="pixels to move")
    parser.add_argument("--delay", type=float, default=0.5, help="seconds between moves")
    parser.add_argument("--count", type=int, default=0, help="cycles, 0 = forever")
    args = parser.parse_args()

    # let the mouse move freely; disable the corner fail-safe
    pyautogui.FAILSAFE = False

    cycles = 0
    print("Moving mouse left/right. Press Ctrl+C to stop.")
    try:
        while args.count == 0 or cycles < args.count:
            pyautogui.moveRel(args.distance, 0, duration=0.2)   # right
            time.sleep(args.delay)
            pyautogui.moveRel(-args.distance, 0, duration=0.2)  # left
            time.sleep(args.delay)
            cycles += 1
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
