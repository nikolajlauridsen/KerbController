
class Screen:
    def __init__(self, fps=10):
        self.fps = fps

    @property
    def delay(self):
        if hasattr(self, 'fps'):
            if self.fps:
                return 1/self.fps
        else:
            return None

    @delay.setter
    def delay(self, delay):
        self.fps = 1/delay

    @delay.deleter
    def delay(self):
        self.fps = None
