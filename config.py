from enum import Enum, auto


class UI_OUT(Enum):
    SD11306 = auto()
    STATIC_IMAGE = auto()
    PYGAME = auto()


class Config:
    DISPLAY_WIDTH = 128
    DISPLAY_HEIGHT = 64
    DISPLAY_IMAGE_MODE = "1"
    UI_OUT = UI_OUT.PYGAME
    ENABLE_CLI = True
    I2C_DISPLAY_ADDR = 0x3c
    PYGAME_IMAGE_MODE = 'RGBA'
