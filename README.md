# move-mouse

Move the mouse cursor left and right repeatedly. Useful for keeping a machine awake.

## Requirements

- Python 3
- [pyautogui](https://pyautogui.readthedocs.io/)

## Setup

```bash
uv venv
uv pip install pyautogui
```

> On macOS, grant Accessibility permission the first time:
> **System Settings → Privacy & Security → Accessibility** → enable your terminal app.

## Usage

```bash
.venv/bin/python move-mouse.py
```

Or activate the venv first:

```bash
source .venv/bin/activate
python move-mouse.py
```

### Options

| Flag         | Default | Description                          |
|--------------|---------|--------------------------------------|
| `--distance` | `200`   | Pixels to move left/right            |
| `--delay`    | `0.5`   | Seconds between each move            |
| `--count`    | `0`     | Number of left-right cycles (0 = forever) |

### Examples

```bash
python move_mouse.py                            # default, runs forever
python move_mouse.py --distance 300 --delay 1   # bigger steps, slower
python move_mouse.py --count 10                 # stop after 10 cycles
```

Stop anytime with `Ctrl+C`.
