from enum import Enum, auto


class UI_OUT(Enum):
    SD11306 = auto()
    STATIC_IMAGE = auto()
    PYGAME = auto()


class Config:
    DISPLAY_WIDTH = 128
    DISPLAY_HEIGHT = 64
    DISPLAY_IMAGE_MODE = "P"
    UI_OUT = UI_OUT.PYGAME
    ENABLE_CLI = True
