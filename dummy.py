from scene import Manager as SceneManager, Scene, DisplayScene
from io_event import IOEvent
from scenes import SceneId
from set_interval import set_interval
from datetime import datetime


class Dummy(DisplayScene):
    def __init__(self, display):
        super().__init__(SceneId.DUMMY, display)
        self.timer = None
        time = datetime.now()
        self.state = {"time": time}

    def on_mount(self, prev_id):
        def callback():
            time = datetime.now()
            self.set_state({"time": time})

        self.timer = set_interval(0.05, callback)

    def on_unmount(self, next_id):
        self.timer.cancel()

    def render(self, state):
        d = self.display

        def display_update(draw):
            d.draw_topbar_text(str(self.state['time']))

        d.use_draw(display_update)
        d.show()
