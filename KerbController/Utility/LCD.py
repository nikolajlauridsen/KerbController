
class Screen:
    def __init__(self, serial, fps=10, size=(16, 2)):
        self.fps = fps
        self.prev_msg = ''
        self.con = serial
        self.size = size

    @property
    def delay(self):
        if hasattr(self, 'fps'):
            if self.fps:
                return 1/self.fps

    @delay.setter
    def delay(self, delay):
        self.fps = 1/delay

    @delay.deleter
    def delay(self):
        self.fps = None

    def flip(self, msg):
        pass

    def compare_message(self, msg):
        """
        Compare the passed string to the last send string, returns a list
        containing the changed fields and their locations, in the format:
        c = changed char, x = x pos on screen, y = y pos on screen
        (example with three chars)
        [('c1', (x,y)), ('c', (x,y)), ('c', (x,y))]
        :param msg: message to be compared
        :return: List of tuples containing ('char', (x,y)) returns None if no changes.
        """
        lines = msg.split('\n')
        # Padding the strings to fit 16 slots means we don't have to worry about short strings
        for i in range(len(lines)):
            if len(lines[i]) < self.size[0]:
                lines[i] += " " * (self.size[0] - len(lines))
        buffer = []

        for n in range(self.size[1]):
            if n < len(lines):
                for i in range(self.size[0]):
                    if i < len(lines[n]):
                        try:
                            if lines[n][i] != self.prev_msg[n][i]:
                                pos = (i, n)
                                buffer.append((lines[n][i], pos))
                        except IndexError:
                            # In the first pass it will throw and index error
                            # since there's an empty string, just add the new char
                            pos = (i, n)
                            buffer.append((lines[n][i], pos))

        if len(buffer) > 0:
            self.prev_msg = lines
            return buffer
        else:
            return None
