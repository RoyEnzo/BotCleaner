from alphabot2 import AlphaBot2

class Controller:

    CMD_FORWARD = "forward"
    CMD_BACKWARD = "backward"
    CMD_TURN_LEFT = "turn_left"
    CMD_TURN_RIGHT = "turn_right"
    CMD_STOP = "stop"

    def __init__(self,alphabot):
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
