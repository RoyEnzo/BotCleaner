from alphabot2 import AlphaBot2
from math import sqrt, pow

class Controller:

    CMD_FORWARD = "forward"
    CMD_BACKWARD = "backward"
    CMD_TURN_LEFT = "turn_left"
    CMD_TURN_RIGHT = "turn_right"
    CMD_STOP = "stop"
    CMD_SPEED = "speed="
    CMD_SEPARATOR = '='

    def __init__(self,alphabot: AlphaBot2):
        self.alphabot = alphabot

    def command(self, cmd):
        """ Convertit commande en action alphabot2"""
        print(cmd)
        if cmd == self.CMD_FORWARD:
            self.alphabot.forward()
        elif cmd == self.CMD_BACKWARD:
            self.alphabot.backward()
        elif cmd == self.CMD_TURN_LEFT:
            self.alphabot.turn_left()
        elif cmd == self.CMD_TURN_RIGHT:
            self.alphabot.turn_right()
        elif cmd == self.CMD_STOP:
            self.alphabot.stop()
        elif self.CMD_SPEED in cmd:
            dutycycle = int(cmd.split(self.CMD_SEPARATOR)[1])

            if 0 <= dutycycle <= 100:
                self.alphabot.dc_left = dutycycle
                self.alphabot.dc_right = dutycycle
                self.alphabot.dc = dutycycle


    def follow_object(self,center,object_coords, distance):
        y0,x0,y1,x1 = object_coords
        y_center, x_center = center
        duty_cycle = self.alphabot.dc

        self.alphabot.stop()

        if min(object_coords) <= 0:
            self.alphabot.set_duty_cycle(duty_cycle,-duty_cycle)
        else:

            deviation_pourcentage = distance / x_center
            deviation_duty_cycle = int(duty_cycle - duty_cycle*deviation_pourcentage)

            print("=====================")
            print("distance : ", distance)
            print("center : ")
            print("deviation : ", deviation_pourcentage, "%")
            print("deviation : ", deviation_duty_cycle, "dc")

            if x0 < x_center:
                print('direction : right')
                self.alphabot.set_duty_cycle(duty_cycle,deviation_duty_cycle)
            else:
                print('direction : left')
                self.alphabot.set_duty_cycle(deviation_duty_cycle,duty_cycle)




