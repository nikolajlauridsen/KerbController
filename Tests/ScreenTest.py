import unittest
from KerbController.Utility.LCD import Screen
import time


class ScreenTest(unittest.TestCase):

    def setUp(self):
        self.screen = Screen(fps=10, serial=None)

    def tearDown(self):
        self.screen.fps = 10

    def test_fps_set(self):
        test_fps = 20
        target_delay = 1/test_fps
        self.screen.fps = 20
        self.assertEqual(self.screen.fps, test_fps)
        self.assertEqual(self.screen.delay, target_delay)

    def test_delay_set(self):
        test_delay = 0.5
        target_fps = 1 / 0.5
        self.screen.delay = test_delay
        self.assertEqual(self.screen.delay, test_delay)
        self.assertEqual(self.screen.fps, target_fps)

    def test_fps_del(self):
        del self.screen.fps
        self.assertEqual(hasattr(self.screen, 'fps'), False)
        self.assertEqual(self.screen.delay, None)

    def test_delay_del(self):
        del self.screen.delay
        self.assertEqual(self.screen.fps, None)
        self.assertEqual(self.screen.delay, None)

    def test_compare(self):
        base_string = 'Hello world!\nLine 2 is here'
        expected_result = [('H', (0, 0)), ('e', (1, 0)), ('l', (2, 0)),
                           ('l', (3, 0)), ('o', (4, 0)), (' ', (5, 0)),
                           ('w', (6, 0)), ('o', (7, 0)), ('r', (8, 0)),
                           ('l', (9, 0)), ('d', (10, 0)), ('!', (11, 0)),
                           (' ', (12, 0)), (' ', (13, 0)), (' ', (14, 0)),
                           (' ', (15, 0)), ('L', (0, 1)), ('i', (1, 1)),
                           ('n', (2, 1)), ('e', (3, 1)), (' ', (4, 1)),
                           ('2', (5, 1)), (' ', (6, 1)), ('i', (7, 1)),
                           ('s', (8, 1)), (' ', (9, 1)), ('h', (10, 1)),
                           ('e', (11, 1)), ('r', (12, 1)), ('e', (13, 1)),
                           (' ', (14, 1)), (' ', (15, 1))]
        comparrison = self.screen.compare_message(base_string)
        self.assertEqual(comparrison, expected_result)

        new_string = 'Hello kerbal!\nLine x is here'
        comparrison = self.screen.compare_message(new_string)
        expected_result = [('k', (6, 0)), ('e', (7, 0)), ('b', (9, 0)),
                           ('a', (10, 0)), ('l', (11, 0)), ('!', (12, 0)),
                           ('x', (5, 1))]
        self.assertEqual(comparrison, expected_result)

        short_string = 'Hi\nworld'
        expected_result = [('i', (1, 0)), (' ', (2, 0)), (' ', (3, 0)),
                           (' ', (4, 0)), (' ', (6, 0)), (' ', (7, 0)),
                           (' ', (8, 0)), (' ', (9, 0)), (' ', (10, 0)),
                           (' ', (11, 0)), (' ', (12, 0)), ('w', (0, 1)),
                           ('o', (1, 1)), ('r', (2, 1)), ('l', (3, 1)),
                           ('d', (4, 1)), (' ', (5, 1)), (' ', (7, 1)),
                           (' ', (8, 1)), (' ', (10, 1)), (' ', (11, 1)),
                           (' ', (12, 1)), (' ', (13, 1))]
        self.assertEqual(self.screen.compare_message(short_string), expected_result)

    def test_ready(self):
        # Setting fps really high to make the test run faster
        self.screen.fps = 1000000
        # Screen should be ready from init
        self.assertEqual(self.screen.ready, True)
        # Simulate transmission
        self.screen._last_transmit = time.time()
        # Shouldn't be allowed to transmit right away
        self.assertEqual(self.screen.ready, False)
        # But after the delay has passed it should be
        time.sleep(0.000001)
        self.assertEqual(self.screen.ready, True)


if __name__ == '__main__':
    unittest.main()
