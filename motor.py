import RPi.GPIO as GPIO


class Motor:
    """ Classe pour moteur N20 du AlphaBot2 """

    def __init__(self, in1, in2, in_pwm, frequency):
        self.IN1 = in1
        self.IN2 = in2
        self.IN_PWM = in_pwm
        self.FREQUENCY = frequency

        GPIO.setup(self.IN1, GPIO.OUT)
        GPIO.setup(self.IN2, GPIO.OUT)
        GPIO.setup(self.IN_PWM, GPIO.OUT)

        self.pwm = GPIO.PWM(self.IN_PWM, self.FREQUENCY)
        self.pwm.start(0)

    def change_duty_cycle(self, duty_cycle):
        """ Change le rapport cyclique du moteur """
        self.pwm.ChangeDutyCycle(duty_cycle)

    def rotate_counterclockwise(self, duty_cycle):
        """ Tourne le moteur dans le sens antihoraire """
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        self.change_duty_cycle(duty_cycle)


    def rotate_clockwise(self, duty_cycle):
        """ Tourne le moteur dans le sens horaire """
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        self.change_duty_cycle(duty_cycle)

    def stop(self):
        """ Arrete le moteur """
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.LOW)
        self.change_duty_cycle(0)

    def __del__(self):
        GPIO.cleanup()

