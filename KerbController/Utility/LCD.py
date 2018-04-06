
class Screen:
    def __init__(self, fps=10):
        self.fps = fps
        self.delay = float

    @property
    def fps(self):
        return self.fps

    @fps.setter
    def fps(self, fps):
        self.delay = 1 / fps
        self.fps = fps

    @fps.deleter
    def fps(self):
        self.delay = None
        return None

