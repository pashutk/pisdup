from scene import Manager as SceneManager, Scene, DisplayScene
from io_event import IOEvent
from scenes import SceneId
from set_interval import set_interval
from datetime import datetime
from time import time
import math


class Loading(DisplayScene):
    def __init__(self, display):
        super().__init__(SceneId.LOADING, display)
        self.timer = None
        start_time = time()
        self.state = {"time": time(), "start_time": start_time}

    def on_mount(self, prev_id):
        def callback():
            self.set_state({"time": time()})

        self.timer = set_interval(0.05, callback)

    def on_unmount(self, next_id):
        self.timer.cancel()

    def render(self, state):
        d = self.display
        x = math.sin(state['time'] * 2.0) * 64 + 64

        def display_update(draw):
            d.draw_centered_text("Scanning for devices")
            draw.line((x, 0, x, 64), 255)

        d.use_draw(display_update)
        d.show()
