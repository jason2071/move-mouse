#!/usr/bin/env python3
"""Simple GUI to move the mouse left and right.

Run:
    .venv/bin/python gui.py
"""
import signal
import sys
import threading
import tkinter as tk
from tkinter import ttk

import config

try:
    import pyautogui
except ImportError:
    sys.exit("pyautogui not installed. Run: uv pip install pyautogui")

try:
    from pynput import keyboard
except ImportError:
    sys.exit("pynput not installed. Run: uv pip install pynput")


pyautogui.FAILSAFE = False


class MouseMoverGUI:
    def __init__(self, root):
        self.root = root
        self.stop_event = threading.Event()
        self.thread = None

        root.title("Move Mouse")
        root.resizable(False, False)

        # global ESC listener (works even when the window is not focused)
        self.key_listener = keyboard.Listener(on_press=self._on_key)
        self.key_listener.start()
        # also stop on ESC when the window is focused
        root.bind("<Escape>", lambda e: self.stop())

        frame = ttk.Frame(root, padding=16)
        frame.grid()

        # distance
        ttk.Label(frame, text="Distance (px)").grid(row=0, column=0, sticky="w", pady=4)
        self.distance = tk.IntVar(value=config.DEFAULT_DISTANCE)
        ttk.Entry(frame, textvariable=self.distance, width=10).grid(row=0, column=1, pady=4)

        # delay
        ttk.Label(frame, text="Delay (s)").grid(row=1, column=0, sticky="w", pady=4)
        self.delay = tk.DoubleVar(value=config.DEFAULT_DELAY)
        ttk.Entry(frame, textvariable=self.delay, width=10).grid(row=1, column=1, pady=4)

        # buttons
        self.start_btn = ttk.Button(frame, text="Start", command=self.start)
        self.start_btn.grid(row=2, column=0, pady=(12, 0), sticky="ew")
        self.stop_btn = ttk.Button(frame, text="Stop", command=self.stop, state="disabled")
        self.stop_btn.grid(row=2, column=1, pady=(12, 0), sticky="ew")

        # status
        self.status = tk.StringVar(value="Idle")
        ttk.Label(frame, textvariable=self.status, foreground="gray").grid(
            row=3, column=0, columnspan=2, pady=(12, 0)
        )

        root.protocol("WM_DELETE_WINDOW", self.on_close)

    def _on_key(self, key):
        # called from the pynput thread; hand off to the Tk main thread
        if key == keyboard.Key.esc:
            self.root.after(0, self.stop)

    def _loop(self, distance, delay):
        # start from the middle of the monitor
        screen_w, screen_h = pyautogui.size()
        pyautogui.moveTo(screen_w // 2, screen_h // 2, duration=0.2)
        while not self.stop_event.is_set():
            pyautogui.moveRel(distance, 0, duration=0.2)   # right
            if self.stop_event.wait(delay):
                break
            pyautogui.moveRel(-distance, 0, duration=0.2)  # left
            if self.stop_event.wait(delay):
                break

    def start(self):
        if self.thread and self.thread.is_alive():
            return
        try:
            distance = int(self.distance.get())
            delay = float(self.delay.get())
        except (tk.TclError, ValueError):
            self.status.set("Invalid input")
            return

        self.stop_event.clear()
        self.thread = threading.Thread(
            target=self._loop, args=(distance, delay), daemon=True
        )
        self.thread.start()
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.status.set("Running…")

    def stop(self):
        self.stop_event.set()
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self.status.set("Stopped")

    def center_window(self):
        """Place the window in the middle of the screen."""
        # hide while we compute geometry so it doesn't flash at the top-left
        self.root.withdraw()
        self.root.update_idletasks()  # ensure the window size is calculated
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        x = (screen_w - w) // 2
        y = (screen_h - h) // 2
        self.root.geometry(f"+{x}+{y}")
        self.root.deiconify()  # show it, already positioned

    def on_close(self):
        self.stop_event.set()
        self.key_listener.stop()
        self.root.destroy()


def main():
    root = tk.Tk()
    app = MouseMoverGUI(root)
    app.center_window()

    # let Ctrl+C in the terminal close the program cleanly
    signal.signal(signal.SIGINT, lambda *_: app.on_close())
    # poll periodically so Python can process the signal while Tk runs
    def _tick():
        root.after(200, _tick)
    root.after(200, _tick)

    root.mainloop()


if __name__ == "__main__":
    main()
