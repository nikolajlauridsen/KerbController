from KerbController.FlightController import FlightController
from KerbController.help import mapvalue

Controller = FlightController('COM4', 9600)
Kerb = FlightController.connect_krpc('FlightController')


@Controller.register_input_command('go')
def stage(*args):
    Controller.get_ship(Kerb).control.activate_next_stage()
    print('Stage activated.')


@Controller.register_input_command('t')
def throttle(*args):
    throt = float(args[0])/100
    Controller.get_ship(Kerb).control.throttle = throt
    print('Throttle set to: ', throt)


Controller.set_variable('prevYaw', 0)
Controller.set_variable('prevPitch', 0)


@Controller.register_input_command('c')
def joystick(*args):
    dead_zone = 0.20
    axi = args[0].split(',')

    yaw = (int(axi[0]) + 25) / 1024
    yaw = mapvalue(yaw, 0, 1, -1, 1)
    if abs(yaw) < dead_zone:
        yaw = 0
    pitch = (int(axi[1]) + 35) / 1024
    pitch = mapvalue(pitch, 0, 1, -1, 1)
    if abs(pitch) < dead_zone:
        pitch = 0
    if yaw != Controller.get_variable('prevYaw'):
        # yaw 0-995
        # pitch 0-985
        print('New  yaw: ', yaw)
        Controller.get_ship(Kerb).control.yaw = yaw
        Controller.set_variable('prevYaw', yaw)
    if pitch != Controller.get_variable('prevPitch'):
        print('New pitch: ', pitch)
        Controller.get_ship(Kerb).control.pitch = pitch
        Controller.set_variable('prevPitch', pitch)


print('Running main loop.')
Controller.run_loop(fps=120)

