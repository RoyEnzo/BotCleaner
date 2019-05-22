import RPi.GPIO as GPIO


class Wheel:
    """
    Classe pour les roues du AlphaBot2-Base.

    Notes:
        Chaque roues sont actionnées par un moteur N20 6V.

        -Pour faire avancer la roue:
            - Activer le Pin1
            - Désactiver le Pin 2
        -Pour faire reculer la roue:
            - Activer le Pin1
            - Désactiver le Pin 2

    Attributes:
        IN_1 (int):
            Pin avancer roue
        IN_2 (int):
            Pin reculer roue
        IN-PWM (int):
            Pin pwm
        FREQUENCY (int):
            Frequence du pwm

    Methods:
        change_duty_cycle(duty_cycle):
            Change le rapport cyclique
        forward(duty_cycle):
            Avance la roue
        backward(duty_cycle):
            Recule la roue
        stop():
            Arrête la roue
    """

    def __init__(self, in_1, in_2, in_pwm, frequency, reverse):
        """
        Initialise une nouvelle roue.

        Notes:
            Puisque l'un des moteurs est montés dans l'autre sens sur le AlphaBot2-Base,
            son fonctionnement dois être inversé.

        Args:
            in_1 (int): Pin de sortie 1.
            in_2 (int): Pin de sortie 2.
            in_pwm (int): Pin de sortie pwm.
            frequency (int): Frequence de pwm.
            reverse (bool): Moteur inversé ?
        """

        if reverse:
            self.IN_1 = in_2
            self.IN_2 = in_1
        else:
            self.IN_1 = in_1
            self.IN_2 = in_2

        self.IN_PWM = in_pwm
        self.FREQUENCY = frequency

        GPIO.setup(self.IN_1, GPIO.OUT)
        GPIO.setup(self.IN_2, GPIO.OUT)
        GPIO.setup(self.IN_PWM, GPIO.OUT)

        self.pwm = GPIO.PWM(self.IN_PWM, self.FREQUENCY)
        self.pwm.start(0)

    def change_duty_cycle(self, duty_cycle):
        """
        Change le rapport cyclique du moteur

        Args:
            duty_cycle (int): rapport cyclique (0-100)
        """
        self.pwm.ChangeDutyCycle(duty_cycle)

    def forward(self, duty_cycle):
        """
        Fait tourner la roue vers l'avant selon un rapport cyclique

        Args:
            duty_cycle (int): rapport cyclique (0-100)
        """
        GPIO.output(self.IN_1, GPIO.HIGH)
        GPIO.output(self.IN_2, GPIO.LOW)
        self.change_duty_cycle(duty_cycle)


    def backward(self, duty_cycle):
        """
        Fait tourner la roue vers l'arrière selon un rapport cyclique

        Args:
            duty_cycle (int): rapport cyclique (0-100)
        """
        GPIO.output(self.IN_1, GPIO.LOW)
        GPIO.output(self.IN_2, GPIO.HIGH)
        self.change_duty_cycle(duty_cycle)

    def stop(self):
        """
        Arrête la roue

        Notes:
            Le rapport cyclique est à 0
        """
        GPIO.output(self.IN_1, GPIO.LOW)
        GPIO.output(self.IN_2, GPIO.LOW)
        self.change_duty_cycle(0)
