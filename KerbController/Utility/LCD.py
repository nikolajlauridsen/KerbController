import time


class Screen:
    def __init__(self, serial, fps=10, size=(16, 2)):
        self.fps = fps
        self.prev_msg = ''
        self.con = serial
        self.size = size
        self._last_transmit = 0

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

    @property
    def ready(self):
        if time.time() - self._last_transmit >= self.delay:
            return True
        else:
            return False

    def flip(self, msg):
        """
        Compare and transmit the passed message, if time between frame has passed
        :param msg: Message to be compared and transmitted
        :return: bool determining if message was sent.
        """
        if self.ready:
            msg = self.compare_message(msg)
            if msg:
                self.send_message(msg)
                return True
        # Nothing was sent return false
        return False

    def send_message(self, compared_msg):
        """
        Send the compared data over serial
        Sends the message as two commands, one ordering to modify screen
        and one with the actual data, which is ended with 255
        :param compared_msg: list generated from self.compare_message
        :return:
        """
        # 1: Send scr command
        # 2: send x coord as byte
        # 3: send y coord as byte
        # 4: send character as character
        # 5. Repeat from 2 for all characters
        # 6. end command by sending a newline
        self.con.write('scr\n'.encode('ascii'))
        for char_pair in compared_msg:
            self.con.write(char_pair[1][0].to_bytes(1, 'big', signed=False))
            self.con.write(char_pair[1][1].to_bytes(1, 'big', signed=False))
            self.con.write(char_pair[0].encode('ascii'))
        self.con.write(0xff)
        self._last_transmit = time.time()

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
