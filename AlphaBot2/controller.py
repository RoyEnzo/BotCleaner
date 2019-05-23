from alphabot2 import AlphaBot2

class Controller:
    """
    Classe permettant de contrôler le robot en fonction des commandes
    reçues par l'application WEB ou l'analyseur d'image.

    Notes:
        Les différentes commandes possible:
            "forward"
                Robot avance.
            "backward"
                Robot recule.
            "turn_left"
                Robot tourne a gauche.
            "turn_right"
                Robot tourne a droite.
            "stop"
                Robot s'arrête.
            "speed=XXX"
                Change la vitesse du robot.
                Remplacer XXX par la vitesse 0-100.

    Attributes:
        alphabot (Alphabot2):
            Robot AlphaBot2 à contrôler.

    Methods:
        command(cmd)
            Commande string à convertir en actions pour le robot.
        push_object(center, object_coords, distance)
            Algorithme pour pousser un objet hors de la zone.

    """

    CMD_FORWARD = "forward"
    CMD_BACKWARD = "backward"
    CMD_TURN_LEFT = "turn_left"
    CMD_TURN_RIGHT = "turn_right"
    CMD_STOP = "stop"
    CMD_SPEED = "speed="
    CMD_SEPARATOR = '='

    def __init__(self):
        """
        Args:
            alphabot:
                Robot AlphaBot2 à contrôler
        """
        self.alphabot = AlphaBot2()

    def command(self, cmd):
        """
        Convertit les commandes (chaîne de caractères) en action

        Args:
            cmd (str):
                Action que le robot doit faire
        """
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
            duty_cycle = int(cmd.split(self.CMD_SEPARATOR)[1])

            if 0 <= duty_cycle <= 100:
                self.alphabot.dc_left = duty_cycle
                self.alphabot.dc_right = duty_cycle
                self.alphabot.dc = duty_cycle

    def push_object(self, center, object_coords, distance):
        """
        Le robot pousse les objets de la zone

        Notes:
            Fonctionnement de l'alghoritme:
                Coordonnées de l'objet négatif (pas d'objet):
                - Le robot tourne sur lui même
                Coordonnée de l'objet positif (objet présent):
                - Le robot se dirige vers l'objet
                    - Plus la distance entre l'objet et le centre de l'image est grande plus le robot tourne vite

        Args:
            center (tuple):
                Point (y, x) central de l'image
            object_coords:
                Coordonnées (y0, x0, y1, x1) de l'objet
            distance:
                Distance entre le centre de l'objet et le centre de l'image
        """
        y0, x0, y1, x1 = object_coords
        y_center, x_center = center
        duty_cycle = self.alphabot.dc

        self.alphabot.stop()

        if min(object_coords) <= 0:
            self.alphabot.set_duty_cycle(duty_cycle, -duty_cycle)
        else:

            turning_ratio = distance / x_center
            deviation_duty_cycle = int(duty_cycle - duty_cycle * turning_ratio)

            if x0 < x_center:
                self.alphabot.set_duty_cycle(duty_cycle, deviation_duty_cycle)
            else:
                self.alphabot.set_duty_cycle(deviation_duty_cycle, duty_cycle)

            # print("=====================")
            # print("distance      : ", distance)
            # print("center        : ")
            # print("turning ratio : ", turning_ratio, "%")
            # print("deviation     : ", deviation_duty_cycle, "dc")
