import unittest
from KerbController.Utility.LCD import Screen


class ScreenTest(unittest.TestCase):

    def setUp(self):
        self.screen = Screen(fps=10)

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


if __name__ == '__main__':
    unittest.main()
