import RPi.GPIO as GPIO
import math
from motor import Motor

class AlphaBot2:

    BCM_AIN1 = 12       # GPIOs moteur droit (inversion ain1 et ain2 - moteur inverse)
    BCM_AIN2 = 13
    BCM_PWMA = 6        # - puissance
    BCM_BIN1 = 20       # GPIOs moteur gauche
    BCM_BIN2 = 21
    BCM_PWMB = 26       # - puissance
    DEFAULT_DC = 30     # rapport cyclique (0 <= dc <= 100)
    FREQUENCY = 500     # valeur de reference

    def __init__(self):
        self.dc_a = self.DEFAULT_DC
        self.dc_b = self.DEFAULT_DC

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        self.motor_a = Motor(self.BCM_AIN1, self.BCM_AIN2, self.BCM_PWMA, self.FREQUENCY)
        self.motor_b = Motor(self.BCM_BIN2, self.BCM_BIN1, self.BCM_PWMB, self.FREQUENCY) # GPIO BIN1 BIN2 inversé

        self.stop()

    def forward(self):
        """ Active les deux moteurs pour aller en avant """
        self.motor_a.rotate_clockwise(self.dc_a)
        self.motor_b.rotate_counterclockwise(self.dc_b)


    def stop(self):
        """ Desactive les deux moteurs """
        self.motor_a.stop()
        self.motor_b.stop()

    def backward(self):
        """ Active les deux moteurs pour aller en arrière """
        self.motor_a.rotate_counterclockwise(self.dc_a)
        self.motor_b.rotate_clockwise(self.dc_b)


    def turn_left(self):
        """ Active les deux moteurs, B en avant, A en arriere  """
        self.motor_a.rotate_counterclockwise(self.dc_a)
        self.motor_b.rotate_counterclockwise(self.dc_b)


    def turn_right(self):
        """ Active les deux moteurs, B en arriere, A en avant """
        self.motor_a.rotate_clockwise(self.dc_a)
        self.motor_b.rotate_clockwise(self.dc_b)


    def set_duty_cycle_a(self, duty_cycle):
        """ Change le rapport cyclique du moteur A """
        self.dc_a = duty_cycle

        if 0 <= self.dc_a:
            self.motor_a.rotate_clockwise()
        elif 0 >= self.dc_a:
            self.motor_a.rotate_counterclockwise()

        self.pwm_a.ChangeDutyCycle(math.abs(self.dc_a))

    def set_duty_cycle_b(self, duty_cycle):
        """ Change le rapport cyclique du moteur B"""
        self.dc_b = duty_cycle

        if 0 <= self.dc_b:
            self.motor_b.rotate_clockwise()
        elif 0 >= self.dc_b:
            self.motor_b.rotate_counterclockwise()

        self.pwm_b.ChangeDutyCycle(math.abs(self.dc_b))

    def set_duty_cycle(self, left, right):
        """ Change le rapport cyclique du moteur A et B """
        self.set_duty_cycle_a(right)
        self.set_duty_cycle_b(left)
