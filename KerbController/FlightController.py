from functools import wraps
import serial
import time
import krpc
from krpc.error import RPCError


class FlightController:
    def __init__(self, com_port, baud_rate):
        """
        Flight controller parsing commands and executing their associated functions.
        :param com_port: Com port the Arduino is communicating on.
        :param baud_rate: Serial speed.
        :return: None.
        """
        self.controller = serial.Serial(com_port, baud_rate)
        self.input_commands = dict()
        self.output_commands = list()
        self.vars = dict()

    def parse_command(self):
        """
        Read and parse commands from serial.
        Reads each command until new line and splits it at :
        This is done since there's no reason to send strings from the Arduino
        to the master script, and allows for an easy way to pass values.
        All values are parsed to a string.
        :return: parsed command, parsed value.
        """
        cmd = self.controller.readline().decode('utf-8').strip()
        if ':' in cmd:
            return cmd.split(':')
        else:
            return cmd, None

    def send_command(self, command, end='\n'):
        """
        Sends a command over serial.
        Always sends it as a string, and separates commands with newline.
        :param command: command to send
        :param end: end of command, works like end in strings, defaults to newline.
        :return: None.
        """
        if type(command) != str:
            command = str(command)
        self.controller.write(command.encode('utf-8'))
        if end:
            if type(end) != str:
                end = str(end)
            self.controller.write(end.encode('utf-8'))

    def set_variable(self, name, value):
        """
        Create or set a variable in the vars dict,
        is used for persistent variables between loops.
        :param name: Variable name.
        :param value: Variable value.
        :return: None.
        """
        self.vars[name] = value

    def get_variable(self, name):
        """
        Get the value associated with key in the self.vars dict.
        :param name: Name of the variable to retrieve.
        :return: Value of variable.
        """
        return self.vars[name]

    def register_input_command(self, command):
        """
        Decorator function for registering an input command.
        The function defined with the decorator will be run, once the command string
        passed to the decorator occurs on the serial port.
        All registered commands will be passed the value from the command as a string
        (as parsed by parse_command)
        :param command: expected command from serial port.
        """
        def decorator(func):
            self.input_commands[command] = func

            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper
        return decorator

    def register_output_command(self, func):
        """
        Decorator for adding an output command send to the Arduino.
        Simply runs the registered function once per controller loop.
        :param func: function to be wrapped.
        :return: wrapped function.
        """
        self.output_commands.append(func)

        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper

    def run_loop(self, fps=None):
        """
        Run the main loop, and start interpreting commands.
        Should be called at the very end of your controller script.
        :param fps: refresh rate for the loop (ignores execution time ups)
        """
        # Calculate sleep time or set to None if 0.
        if not fps or fps == 0:
            delay = None
        else:
            delay = 1/fps

        while True:
            # Inputs: Keep parsing commands till queue is empty.
            # Allows the controller to activate multiple commands between "frames".
            while self.controller.in_waiting > 0:
                cmd = self.parse_command()
                # Command received, test if it's in our stored commands
                if cmd[0] in self.input_commands.keys():
                    # If it its, run the commands functions.
                    # NOTE: this will pass the value of the command as argument,
                    # It's therefore required for the registered function to handle 1 argument.
                    self.input_commands[cmd[0]](cmd[1])
                else:
                    print('Unknown command received: ', cmd)

            # Outputs.
            for task in self.output_commands:
                task()
            # Limit refresh rate.
            if delay:
                time.sleep(delay)

    @staticmethod
    def connect_krpc(name, **kwargs):
        """
        Keep attempting to connect to the krpc server.
        :param name: Connection name appearing on the krpc plugin.
        :return: krpc object.
        """
        print('Connecting to krpc server...')
        while True:
            try:
                # Try connecting
                conn = krpc.connect(name=name, **kwargs)
            except ConnectionRefusedError:
                # Didn't work, wait a bit and try again
                # TODO: Make non deterministic indicator (I know right)
                print('.')
                time.sleep(0.3)
                continue
            # If we had success return the connection.
            return conn

    @staticmethod
    def get_ship(kerb):
        """
        Return a vessel object from a krpc object.
        Will keep trying to return a ship until it's able to.
        Allows you to wait for a launch.
        :param kerb: krpc object.
        :return: krpc vessel object.
        """
        while True:
            try:
                kerb.space_center.active_vessel.name
            except RPCError:
                time.sleep(0.3)
                continue
            return kerb.space_center.active_vessel
