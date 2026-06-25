# move-mouse

Move the mouse cursor left and right repeatedly. Useful for keeping a machine awake.
Comes with both a **CLI** and a **GUI**.

## Requirements

- Python 3
- [pyautogui](https://pyautogui.readthedocs.io/)
- [pynput](https://pynput.readthedocs.io/)

## Setup

```bash
make setup
```

Or manually:

```bash
uv venv
uv pip install pyautogui pynput
```

> On macOS, grant Accessibility permission the first time:
> **System Settings → Privacy & Security → Accessibility** → enable your terminal app.

## Make commands

| Command      | Description                                   |
|--------------|-----------------------------------------------|
| `make setup` | Create venv and install dependencies          |
| `make run`   | Run the CLI (`make run ARGS="--distance 300"`) |
| `make gui`   | Run the GUI                                   |
| `make clean` | Remove venv and caches                        |
| `make help`  | List available commands                       |

## CLI

```bash
make run
# or
.venv/bin/python move-mouse.py
```

### Options

| Flag         | Default | Description                          |
|--------------|---------|--------------------------------------|
| `--distance` | `200`   | Pixels to move left/right            |
| `--delay`    | `0.5`   | Seconds between each move            |
| `--count`    | `0`     | Number of left-right cycles (0 = forever) |

### Examples

```bash
make run                                    # default, runs forever
make run ARGS="--distance 300 --delay 1"    # bigger steps, slower
make run ARGS="--count 10"                  # stop after 10 cycles
```

Stop anytime with **ESC**, **right-click**, or `Ctrl+C`.

## GUI

```bash
make gui
# or
.venv/bin/python gui.py
```

Set **Distance** and **Delay**, then click **Start** / **Stop**.

Stop anytime with **ESC** (works even when the window is not focused),
by closing the window, or with `Ctrl+C` in the terminal.
