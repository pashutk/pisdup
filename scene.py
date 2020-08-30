
from pyee import BaseEventEmitter
from enum import Enum, auto


# class Event(Enum):
#     MOUNT = auto()
#     UNMOUNT = auto()


class Manager:
    def __init__(self):
        self.scenes = {}
        self.current = None

    def register_scene(self, scene):
        id = scene.id
        if id in self.scenes:
            raise Exception(
                "Cannot register already registered scene {}".format(id))

        self.scenes[scene.id] = scene

    def go(self, scene_id):
        if not scene_id in self.scenes:
            raise Exception("Trying to run unknown scene {}".format(scene_id))

        next_scene = self.scenes[scene_id]
        prev_scene_id = None
        if self.current:
            prev_scene_id = self.current.id
            self.current.unmount(scene_id)

        self.current = next_scene
        self.current.mount(prev_scene_id)

    def destroy(self):
        if self.current:
            self.current.unmount()


class Scene:
    def __init__(self, id):
        self.id = id
        self.state = {}

    def set_state(self, new_state):
        merged = {**self.state, **new_state}
        if self.state == merged:
            return

        self.state = merged
        self.render(self.state)

    def mount(self, prev_id):
        self.on_mount(prev_id)
        self.render(self.state)

    def unmount(self, next_id=None):
        self.on_unmount(next_id)

    def render(self, state):
        pass

    def on_mount(self, prev_id):
        pass

    def on_unmount(self, next_id):
        pass


class DisplayScene(Scene):
    def __init__(self, id, display):
        super().__init__(id)
        self.display = display
