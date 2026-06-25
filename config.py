"""Shared configuration loaded from environment variables and an optional .env file.

Precedence (highest first):
    1. CLI arguments (handled by each script)
    2. environment variables / .env file
    3. built-in defaults below

Recognised variables:
    MOVE_DISTANCE  pixels to move left/right   (default 200)
    MOVE_DELAY     seconds between each move    (default 0.5)
    MOVE_COUNT     left-right cycles, 0=forever (default 0)
"""
import os

try:
    from dotenv import load_dotenv
    load_dotenv()  # read a .env file in the current directory, if present
except ImportError:
    # python-dotenv is optional; plain environment variables still work
    pass


DEFAULT_DISTANCE = int(os.environ.get("MOVE_DISTANCE", 200))
DEFAULT_DELAY = float(os.environ.get("MOVE_DELAY", 0.5))
DEFAULT_COUNT = int(os.environ.get("MOVE_COUNT", 0))
