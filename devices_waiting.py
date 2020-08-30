from scene import Manager as SceneManager, Scene, DisplayScene
from io_event import IOEvent
from scenes import SceneId
from set_interval import set_interval


class DevicesWaiting(DisplayScene):
    def __init__(self, display, io_ee):
        super().__init__(SceneId.DEVICES_WAITING, display)
        self.io_ee = io_ee
        self.dots_timer = None
        self.state = {"hdd_inserted": False,
                      "sd_inserted": False, "dots_count": 1}

    def on_mount(self, prev_id):
        self.io_ee.on(IOEvent.INSERT_SD, self.on_insert_sd)
        self.io_ee.on(IOEvent.INSERT_HDD, self.on_insert_hdd)
        self.io_ee.on(IOEvent.EJECT_HDD, self.on_eject_hdd)
        self.io_ee.on(IOEvent.EJECT_SD, self.on_eject_sd)

        def callback():
            count = self.state["dots_count"]
            if count == 3:
                count = -1

            self.set_state({"dots_count": count + 1})

        self.dots_timer = set_interval(1.0, callback)

    def on_unmount(self, next_id):
        self.io_ee.remove_listener(IOEvent.INSERT_SD, self.on_insert_sd)
        self.io_ee.remove_listener(IOEvent.INSERT_HDD, self.on_insert_hdd)
        self.io_ee.remove_listener(IOEvent.EJECT_HDD, self.on_eject_hdd)
        self.io_ee.remove_listener(IOEvent.EJECT_SD, self.on_eject_sd)

        self.dots_timer.cancel()

    def on_insert_sd(self):
        self.set_state({"sd_inserted": True})

    def on_insert_hdd(self):
        self.set_state({"hdd_inserted": True})

    def on_eject_sd(self):
        self.set_state({"sd_inserted": False})

    def on_eject_hdd(self):
        self.set_state({"hdd_inserted": False})

    def render(self, state):
        lines = []
        if state['hdd_inserted'] == False:
            lines.append("Connect HDD")
        if state['sd_inserted'] == False:
            lines.append("Insert SD")

        lines_with_dots = map(lambda line: line + "." *
                              state["dots_count"], lines)
        d = self.display

        def display_update(draw):
            d.draw_topbar_text("Waiting for devices")
            top = 16
            for line in lines_with_dots:
                d.draw_white_text((5, top), line)
                top = top + 10

        d.use_draw(display_update)
        d.show()
