# import pyudev
from enum import Enum, auto
import time
from pyee import BaseEventEmitter
from config import Config
from display import Display
from cli import Cli
from scene import Manager as SceneManager
from io_event import IOEvent
from devices_waiting import DevicesWaiting
from scenes import SceneId
from dummy import Dummy
from loading import Loading


class MainAppState(Enum):
    INIT = auto()
    WAITING_FOR_DEVICES = auto()


class App:
    def __init__(self):
        self.state = MainAppState.INIT
        self.display = Display()
        self.ee = BaseEventEmitter()
        self.cli = None
        if Config.ENABLE_CLI:
            self.cli = Cli()

    def init(self):
        if Config.ENABLE_CLI:
            self.cli.run()

    def handle_cli_command(self, input_str):
        command_up = "up"
        command_ok = "ok"
        command_down = "down"

        if input_str == command_ok or input_str == command_up or input_str == command_down:
            self.ee.emit(IOEvent.BUTTON)

        if (input_str == command_up):
            self.ee.emit(IOEvent.BUTTON_UP)

        if (input_str == command_down):
            self.ee.emit(IOEvent.BUTTON_DOWN)

        if (input_str == command_ok):
            self.ee.emit(IOEvent.BUTTON_OK)

        if (input_str == "isd"):
            self.ee.emit(IOEvent.INSERT_SD)

        if (input_str == "ihd"):
            self.ee.emit(IOEvent.INSERT_HDD)

        if (input_str == "esd"):
            self.ee.emit(IOEvent.EJECT_SD)

        if (input_str == "ehd"):
            self.ee.emit(IOEvent.EJECT_HDD)

    def run(self):
        self.init()

        sm = SceneManager()

        sm.register_scene(DevicesWaiting(self.display, self.ee))

        # sm.go(SceneId.DEVICES_WAITING)
        sm.register_scene(Dummy(self.display))
        # sm.go(SceneId.DUMMY)

        sm.register_scene(Loading(self.display))
        sm.go(SceneId.LOADING)

        while (True):
            if Config.ENABLE_CLI:
                input_str = self.cli.read()
                if input_str == 'exit':
                    sm.destroy()
                    break
                self.handle_cli_command(input_str)

            time.sleep(0.01)


# context = pyudev.Context()
# monitor = pyudev.Monitor.from_netlink(context)
# monitor.filter_by('block')
# for device in iter(monitor.poll, None):
#     if 'ID_FS_TYPE' in device:
#         print('{0} partition {1}, {2}'.format(
#             device.action, device.get('ID_FS_LABEL'), device.device_node))
# #

# monitor = pyudev.Monitor.from_netlink(context)
# monitor.filter_by('block')


# def log_event(action, device):
#     if 'ID_FS_TYPE' in device:
#         with open('filesystems.log', 'a+') as stream:
#             print('{0} - {1}'.format(action,
#                                      device.get('ID_FS_LABEL')), file=stream)


# observer = pyudev.MonitorObserver(monitor, log_event)
# observer.start()
