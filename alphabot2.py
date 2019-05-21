import RPi.GPIO as GPIO
from wheel import Wheel

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
        self.dc_left = self.DEFAULT_DC
        self.dc_right = self.DEFAULT_DC

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        self.motor_left = Wheel(self.BCM_AIN1, self.BCM_AIN2, self.BCM_PWMA, self.FREQUENCY, True)  # Moteur a l'envers
        self.motor_right = Wheel(self.BCM_BIN1, self.BCM_BIN2, self.BCM_PWMB, self.FREQUENCY,True)

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
        print("left")
        self.motor_right.forward(self.dc_right)
        print("right")


    def turn_right(self):
        """ Active les deux moteurs, B en arriere, A en avant """
        self.motor_left.forward(self.dc_left)
        self.motor_right.backward(self.dc_right)


    def set_duty_cycle_a(self, duty_cycle):
        """ Change le rapport cyclique du moteur A """
        self.dc_left = duty_cycle

        if 0 <= self.dc_left:
            self.motor_left.forward()
        elif 0 >= self.dc_left:
            self.motor_left.backward()

        self.pwm_a.ChangeDutyCycle(abs(self.dc_left))

    def set_duty_cycle_b(self, duty_cycle):
        """ Change le rapport cyclique du moteur B"""
        self.dc_right = duty_cycle

        if 0 <= self.dc_right:
            self.motor_right.forward()
        elif 0 >= self.dc_right:
            self.motor_right.backward()

        self.pwm_b.ChangeDutyCycle(abs(self.dc_right))

    def set_duty_cycle(self, left, right):
        """ Change le rapport cyclique du moteur A et B """
        self.set_duty_cycle_a(right)
        self.set_duty_cycle_b(left)
