import RPi.GPIO as GPIO


class Wheel:

    def __init__(self, in_1, in_2, in_pwm, frequency, reverse):
        """
        Moteur N20 utilisé par AlphaBot2-Base
        Args:
            in_1 (int): pin de sortie 1
            in_2 (int): pin de sortie 2
            in_pwm (int): pin de sortie pwm
            frequency (int): frequence de pwm
            reverse (bool): Is the motor reversed ?
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
        self.pwm.ChangeDutyCycle(duty_cycle)

    def forward(self, duty_cycle):
        GPIO.output(self.IN_1, GPIO.HIGH)
        GPIO.output(self.IN_2, GPIO.LOW)
        print("high")
        self.change_duty_cycle(duty_cycle)


    def backward(self, duty_cycle):
        GPIO.output(self.IN_1, GPIO.LOW)
        GPIO.output(self.IN_2, GPIO.HIGH)
        self.change_duty_cycle(duty_cycle)

    def stop(self):
        GPIO.output(self.IN_1, GPIO.LOW)
        GPIO.output(self.IN_2, GPIO.LOW)
        self.change_duty_cycle(0)

    def __del__(self):
        GPIO.cleanup()

