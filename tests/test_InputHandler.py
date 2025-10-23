from pynput.keyboard import Key, KeyCode, Listener
from unittest.mock import patch
import unittest
from packages.InputHandler import InputHandler, Command, KeyPress
import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)


def run_manual_test():
    handler = InputHandler()
    frame_count = 0
    print("--- Starting Manual Input Test ---")
    print("Press keys bound to commands. Press Ctrl+C to exit.")
    try:
        while True:
            command = handler.get_command()
            if command is not None:
                print(
                    f"Command: {command}, Frames elapsed since last command: {frame_count}")
                frame_count = 0
            else:
                frame_count += 1
    except KeyboardInterrupt:
        print("\n--- Exiting manual test ---")


class TestInputHandler(unittest.TestCase):
    TEST_BINDINGS: dict[KeyPress, Command] = {
        KeyCode.from_char("z"): "UP",
        KeyCode.from_char("q"): "LEFT",
    }

    @patch('packages.InputHandler.Listener')
    def setUp(self, MockListener: Listener):
        self.handler = InputHandler(bindings=self.TEST_BINDINGS)

    def test_initialization_with_provided_bindings(self):
        self.assertEqual(self.handler.bindings, self.TEST_BINDINGS)

    @patch('packages.InputHandler.Listener')
    def test_initialization_with_default_bindings(self, MockListener: Listener):
        default_handler = InputHandler()
        self.assertIsNotNone(default_handler.bindings)
        self.assertIn(KeyCode.from_char("w"), default_handler.bindings)

    def test_get_command_consumes_input(self):
        key_to_press = KeyCode.from_char("z")
        expected_command = self.TEST_BINDINGS[key_to_press]
        self.handler.on_release(key_to_press)
        self.assertEqual(self.handler.get_command(), expected_command)
        self.assertIsNone(self.handler.get_command())

    def test_peek_command_does_not_consume_input(self):
        key_to_press = KeyCode.from_char("q")
        expected_command = self.TEST_BINDINGS[key_to_press]
        self.handler.on_release(key_to_press)
        self.assertEqual(self.handler.get_command(
            peek_key=True), expected_command)
        self.assertEqual(self.handler.get_command(
            peek_key=True), expected_command)
        self.assertEqual(self.handler.get_command(), expected_command)
        self.assertIsNone(self.handler.get_command())

    def test_unbound_keycode_returns_none(self):
        key_to_press = KeyCode.from_char("x")
        self.handler.on_release(key_to_press)
        self.assertIsNone(self.handler.get_command())

    def test_special_key_returns_none(self):
        key_to_press = Key.shift
        self.handler.on_release(key_to_press)
        self.assertIsNone(self.handler.get_command())


if __name__ == '__main__':
    if '--manual' in sys.argv:
        run_manual_test()
    else:
        unittest.main(argv=['first-arg-is-ignored'], exit=False)
