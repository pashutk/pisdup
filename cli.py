import threading
import queue


def read_kbd_input(inputQueue):
    print('CLI ready, input commands')
    while (True):
        input_str = input()
        inputQueue.put(input_str)


class Cli:
    def __init__(self):
        self.inputQueue = queue.Queue()

    def run(self):
        inputThread = threading.Thread(
            target=read_kbd_input, args=(self.inputQueue,), daemon=True)
        inputThread.start()

    def read(self):
        if (self.inputQueue.qsize() > 0):
            return self.inputQueue.get()
