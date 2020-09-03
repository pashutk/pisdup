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

        self.timer = set_interval(0.1, callback)

    def on_unmount(self, next_id):
        self.timer.cancel()

    def render(self, state):
        d = self.display
        x_center = d.image.width // 2
        y_center = d.image.height
        max_r = math.sqrt(pow(x_center, 2) + pow(y_center, 2))

        def n(a):
            return (math.cos(a), math.sin(a))

        def x(a):
            if a == math.pi / 2:
                return (64, 0)
            if a == 0:
                return (0, 64)
            if a == math.pi:
                return (64, 64)

            p1, p2 = n(a)
            x = (0 - y_center) * p1 / p2 + x_center
            return (x, 0)

        def y(a):
            if a == 3 * math.pi / 2:
                return (64, 128)

            p1, p2 = n(a)
            x = (128 - y_center) * p1 / p2 + x_center
            return (x, 128)

        def sqr_xy(r):
            return (x_center - r, y_center - r, x_center + r, y_center + r)

        def display_update(draw):
            d.draw_centered_text("Scanning for devices")

            distance_between = 10

            lines_count = d.image.height // distance_between

            i = state["time"]
            i = i * 100
            i = i % 360

            for line_num in range(1, lines_count + 1):
                draw.arc(sqr_xy(line_num * distance_between),
                         i - 12, i - 11, fill=255, width=1)
                draw.arc(sqr_xy(line_num * distance_between),
                         i - 10, i - 3, fill=255, width=1)
                draw.arc(sqr_xy(line_num * distance_between),
                         i, i + 13, fill=255, width=1)

            # i = state["time"]
            # i = i * 400
            # i = i % 1000
            # i = i / 1000
            # i = i * math.pi * 2
            # if i > math.pi:
            #     # draw.line((64, 64) + y(i), 255)
            #     pass
            # else:
            #     draw.line(x(i) + (64, 64), 255)

            # def hcircle(r):
            #     draw.arc(sqr_xy(r), 180, 360, fill=255, width=1)
            # # draw.line((x_center, 0, x_center, 64), 255)
            # r = state["time"] - state["start_time"]
            # r = r * 50
            # # r = r % max_r
            # # r = pow(r, 2)
            # # r = r * max_r
            # r = r % max_r
            # r = r * max_r
            # r = math.sqrt(r)
            # hcircle(r)

        d.use_draw(display_update)
        d.show()
