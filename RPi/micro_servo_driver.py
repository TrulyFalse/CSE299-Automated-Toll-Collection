import time
import RPi.GPIO as GPIO

class micro_servo:
    def __init__(self, signal_pin_number, signal_frequency, pwm_period, left_duty_time, neutral_duty_time, right_duty_time):
        self.signal_pin_number = signal_pin_number
        self.signal_frequency = signal_frequency
        self.pwm = GPIO.PWM(self.signal_pin_number, self.signal_frequency)

        self.left_duty_percentage = (left_duty_time / pwm_period) * 100
        self.neutral_duty_percentage = (neutral_duty_time / pwm_period) * 100
        self.right_duty_percentage = (right_duty_time / pwm_period) * 100

        self.duty_per_angle = (self.right_duty_percentage - self.left_duty_percentage) / 180

    def set_servo_angle(self, angle):
        self.pwm.start(0)
        if angle >= 0 and angle <= 180:
            self.pwm.ChangeDutyCycle(self.left_duty_percentage + (angle * self.duty_per_angle))
            time.sleep(2) # sparing two seconds for servo to reach position
            self.pwm.stop()
        else:
            print("Angle not supported by servo motor.")


    def open_barrier(self):
        self.set_servo_angle(90)

    def close_barrier(self):
        self.set_servo_angle(0)