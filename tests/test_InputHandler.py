from packages.InputHandler import *
import unittest


class InputHandlerManualTester():
    def test_handle(self):
        handler = InputHandler()
        frame_count = 0
        while True:
            if handler.get_command(True) != None:
                
                print(handler.get_command(), "frames elapsed since last command: ", frame_count)
                frame_count = 0
            frame_count += 1


class RendererTester(unittest.TestCase):
    def func(self):
        pass


if __name__ == "__main__":
    manual = InputHandlerManualTester()
    manual.test_handle()
