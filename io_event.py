from enum import Enum, auto


class IOEvent(Enum):
    INSERT_SD = auto()
    INSERT_HDD = auto()
    EJECT_SD = auto()
    EJECT_HDD = auto()
    BUTTON_UP = auto()
    BUTTON_DOWN = auto()
    BUTTON_OK = auto()
    BUTTON = auto()
