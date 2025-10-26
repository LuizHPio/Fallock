from unittest.mock import patch
import unittest
from packages.InputHandler import InputHandler, Command, KeyPress
import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)


class TestInputHandler(unittest.TestCase):
    TEST_BINDINGS: dict[KeyPress, Command] = {
        "z": "UP",
        "q": "LEFT",
    }

    @patch('packages.InputHandler.keyboard.on_release')
    def setUp(self, MockOnRelease):
        self.handler = InputHandler(bindings=self.TEST_BINDINGS)
        self.mock_on_release_callback = MockOnRelease.call_args[0][0]

    def test_initialization_with_provided_bindings(self):
        self.assertEqual(self.handler.bindings, self.TEST_BINDINGS)

    @patch('packages.InputHandler.keyboard.on_release')
    def test_initialization_with_default_bindings(self, MockOnRelease):
        default_handler = InputHandler()
        self.assertIsNotNone(default_handler.bindings)
        self.assertIn("w", default_handler.bindings)

    def test_get_command_consumes_input(self):
        key_to_press = "z"
        expected_command = self.TEST_BINDINGS[key_to_press]

        mock_event = unittest.mock.MagicMock()
        mock_event.name = key_to_press
        self.mock_on_release_callback(mock_event)

        self.assertEqual(self.handler.get_command(), expected_command)
        self.assertIsNone(self.handler.get_command())

    def test_peek_command_does_not_consume_input(self):
        key_to_press = "q"
        expected_command = self.TEST_BINDINGS[key_to_press]

        mock_event = unittest.mock.MagicMock()
        mock_event.name = key_to_press
        self.mock_on_release_callback(mock_event)

        self.assertEqual(self.handler.get_command(
            peek_key=True), expected_command)
        self.assertEqual(self.handler.get_command(
            peek_key=True), expected_command)
        self.assertEqual(self.handler.get_command(), expected_command)
        self.assertIsNone(self.handler.get_command())

    def test_unbound_keycode_returns_none(self):
        key_to_press = "x"

        mock_event = unittest.mock.MagicMock(name=key_to_press)
        self.mock_on_release_callback(mock_event)

        self.assertIsNone(self.handler.get_command())

    def test_special_key_returns_none(self):
        key_to_press = "shift"

        mock_event = unittest.mock.MagicMock(name=key_to_press)
        self.mock_on_release_callback(mock_event)

        self.assertIsNone(self.handler.get_command())


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
