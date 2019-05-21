from alphabot2 import AlphaBot2

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


    def follow_object(self,image_resolution,object_coords):
        y1,x1,y2,x2 = object_coords
        width, height = image_resolution

        y_center = int(width / 2)
        x_center = int(height / 2)
        y = int((y1 + y2) / 2)
        x = int((x1 + x2) / 2)

