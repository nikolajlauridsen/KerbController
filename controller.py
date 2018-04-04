from KerbController.FlightController import FlightController
from KerbController.help import mapvalue, eng_notate

Controller = FlightController('COM4', 9600)
Kerb = FlightController.connect_krpc('FlightController')

Controller.set_variable('prevYaw', 0)
Controller.set_variable('prevPitch', 0)
Controller.set_variable('prevThrust', '')
Controller.set_variable('prevApoapsis', '')


@Controller.register_input_command('go')
def stage(*args):
    Controller.get_ship(Kerb).control.activate_next_stage()
    print('Stage activated.')


@Controller.register_input_command('t')
def throttle(*args):
    throt = float(args[0])/100
    Controller.get_ship(Kerb).control.throttle = throt
    print('Throttle set to: ', throt)


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


@Controller.register_input_command('sas')
def sas(*args):
    if args[0] == "1":
        Controller.get_ship(Kerb).control.sas = True
        print('SAS Activated.')
    else:
        Controller.get_ship(Kerb).control.sas = False
        print('SAS deactivated.')


@Controller.register_output_command
def screen():
    current_thrust = eng_notate(Controller.get_ship(Kerb).thrust)
    current_apoapsis = eng_notate(Controller.get_ship(Kerb).orbit.apoapsis_altitude)
    if current_thrust != Controller.get_variable('prevThrust') or current_apoapsis != Controller.get_variable('prevaAoapsis'):
        line1_label = 'Thrust: '
        line2_label = 'pk: '
        line1 = '{}{}{}'.format(line1_label, " " * (16-len(line1_label)-len(current_thrust)),
                                current_thrust)

        line2 = '{}{}{}'.format(line2_label, " " * (16 - len(line2_label) - len(current_apoapsis)),
                                current_apoapsis)

        Controller.send_command(line1+line2)
        Controller.set_variable('prevThrust', current_thrust)
        Controller.set_variable('prevaAoapsis', current_apoapsis)


print('Running main loop.')
Controller.run_loop(fps=120)

