import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

class led_set:
    def __init__(self, green_led_pin_number, yellow_led_pin_number, red_led_pin_number):
        self.green_led_pin_number = green_led_pin_number
        self.yellow_led_pin_number = yellow_led_pin_number
        self.red_led_pin_number = red_led_pin_number
        
        GPIO.setup(self.green_led_pin_number, GPIO.OUT)
        GPIO.setup(self.yellow_led_pin_number, GPIO.OUT)
        GPIO.setup(self.red_led_pin_number, GPIO.OUT)

    def turn_green_on(self):
        GPIO.output(self.green_led_pin_number, True)
    def turn_green_off(self):
        GPIO.output(self.green_led_pin_number, False)

    def turn_yellow_on(self):
        GPIO.output(self.yellow_led_pin_number, True)
    def turn_yellow_off(self):
        GPIO.output(self.yellow_led_pin_number, False)

    def turn_red_on(self):
        GPIO.output(self.red_led_pin_number, True)
    def turn_red_off(self):
        GPIO.output(self.red_led_pin_number, False)
