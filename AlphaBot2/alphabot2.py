import RPi.GPIO as GPIO
from wheel import Wheel


class AlphaBot2:
    """
    Classe AlphaBot2-base.
    Déplacement du robot, contrôle des moteurs.

    Notes:
        Reférence de pins GPIO en mode BCM (Broadcom SOC channel).

        Pour créer la classe je me suis aidé des scripts proposés par WaveShare:
        https://www.waveshare.com/wiki/AlphaBot2-Pi#Demo

    Attributes:
        BCM_AIN1 (int):
            Moteur gauche pin 1.
        BCM_AIN2 (int):
            Moteur gauche pin 2.
        BCM_PWMA (int):
            Moteur gauche pin pwm.
        BCM_BIN1  (int):
            Moteur droit pin 1.
        BCM_BIN2  (int):
            Moteur droit pin 2.
        BCM_PWMB  (int):
            Moteur droit pin pwm.
        DEFAULT_DC  (int):
            Moteur rapport cyclique par default (0-100).
        FREQUENCY  (int):
            Frequence du PWM.
        dc_left (int):
            Duty cycle moteur gauche.
        dc_right (int):
            Duty cycle moteur droit.
        dc (int):
            Duty cycle de base.
        motor_left (Wheel):
            Roue gauche.
        motor_right (Wheel):
            Roue droite.

    Methods:
        forward():
            Avance le robot.
        backward():
            Recule le robot.
        turn_left():
            Tourne le robot à gauche.
        turn_right():
            Tourne le robot à droite
        stop():
            Arrête le robot.
        set_duty_cycle_a(duty_cycle):
            Change le rapport cyclique du PWM gauche.
        set_duty_cycle_b(duty_cycle):
            Change le rapport cyclique du PWM droit.
        set_duty_cycle(left, right):
            Change le rapport cyclique du PWM gauche et droite.
        __del__():
            Nettoie les GPIO.
            Assure une fermeture propre.

    """
    BCM_AIN1 = 12
    BCM_AIN2 = 13
    BCM_PWMA = 6
    BCM_BIN1 = 20
    BCM_BIN2 = 21
    BCM_PWMB = 26
    DEFAULT_DC = 50
    FREQUENCY = 500

    def __init__(self):
        """
        Notes:
            Reférence de pins GPIO en mode BCM (Broadcom SOC channel).
            N'affiche pas les avertissements de GPIO.
        """
        self.dc_left = self.DEFAULT_DC
        self.dc_right = self.DEFAULT_DC
        self.dc = self.DEFAULT_DC

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        self.motor_left = Wheel(self.BCM_AIN1, self.BCM_AIN2, self.BCM_PWMA, self.FREQUENCY, True)
        self.motor_right = Wheel(self.BCM_BIN1, self.BCM_BIN2, self.BCM_PWMB, self.FREQUENCY, True)

        self.stop()

    def forward(self):
        """ Active les deux moteurs pour aller en avant """
        self.motor_left.forward(self.dc_left)
        self.motor_right.forward(self.dc_right)

    def stop(self):
        """ Desactive les deux moteurs """
        self.motor_left.stop()
        self.motor_right.stop()

    def backward(self):
        """ Active les deux moteurs pour aller en arrière """
        self.motor_left.backward(self.dc_left)
        self.motor_right.backward(self.dc_right)

    def turn_left(self):
        """ Active les deux moteurs, B en avant, A en arriere  """
        self.motor_left.backward(self.dc_left)
        self.motor_right.forward(self.dc_right)

    def turn_right(self):
        """ Active les deux moteurs, B en arriere, A en avant """
        self.motor_left.forward(self.dc_left)
        self.motor_right.backward(self.dc_right)

    def set_duty_cycle_a(self, duty_cycle):
        """ Change le rapport cyclique du moteur A

        Attributes
            duty_cycle (int):
                rapport cyclique (0-100).
        """
        self.dc_left = duty_cycle

        if 0 <= self.dc_left:
            self.motor_left.forward(abs(duty_cycle))
        elif 0 >= self.dc_left:
            self.motor_left.backward(abs(duty_cycle))

    def set_duty_cycle_b(self, duty_cycle):
        """
        Change le rapport cyclique du moteur B

        Attributes
            duty_cycle (int):
                rapport cyclique (0-100).
        """
        self.dc_right = duty_cycle

        if 0 <= self.dc_right:
            self.motor_right.forward(abs(duty_cycle))
        elif 0 >= self.dc_right:
            self.motor_right.backward(abs(duty_cycle))

    def set_duty_cycle(self, left, right):
        """
        Change le rapport cyclique du moteur A et B

        Attributes
            left (int):
                rapport cyclique (0-100) moteur A.
            right (int):
                rapport cyclique (0-100) moteur B.
        """
        self.set_duty_cycle_a(right)
        self.set_duty_cycle_b(left)

    def __del__(self):
        """ Nettoie les GPIO """
        GPIO.cleanup()
