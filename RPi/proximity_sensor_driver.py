import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# module constants
def SPEED_OF_SOUND():
    return 343 # in m/s

def PRECISION():
    return 0.003 # in metres

def RECOMMENDED_CYCLE_PERIOD():
    return 0.05 # in seconds


class proximity_sensor:
    def __init__(self, trigger_pin_number, echo_pin_number):
        self.trigger_pin_number = trigger_pin_number
        self.echo_pin_number = echo_pin_number

        # defining I/O for sensor
        # TRIGGER: output HIGH to fire ultrasound pulses and LOW to stop firing
        # ECHO: inputs HIGH when the TRIGGER ends and LOW when the echo ends
        GPIO.setup(self.trigger_pin_number, GPIO.OUT)
        GPIO.setup(self.echo_pin_number, GPIO.IN)


    # methods
    # distance in metres
    def distance(self):
        # start sending pulse via transmitter
        GPIO.output(self.trigger_pin_number, True)
    
        # stop pulses after 10 microseconds, recommended by HC-SR04 datasheet
        time.sleep(0.00001)
        GPIO.output(self.trigger_pin_number, False)
    
        # save the time when the echo begins
        while GPIO.input(self.echo_pin_number) == 0:
            start_time = time.time()
    
        # save time when the echo ends
        while GPIO.input(self.echo_pin_number) == 1:
            stop_time = time.time()
        
        # formula from datasheets of HC-SR04 uses echo duration to calculate distances
        echo_duration = stop_time - start_time
        distance = (echo_duration * SPEED_OF_SOUND) / 2
    
        return distance


    # speed in metres per second
    def speed(self):
        start_distance = self.distance()
        time.sleep(RECOMMENDED_CYCLE_PERIOD)
        end_distance = self.distance()

        # positive = moving away from sensor, negative = moving toward sensor 
        speed = (end_distance - start_distance) / RECOMMENDED_CYCLE_PERIOD

        return speed


    def is_stationary(self):
        # false speed that may be detected by the sensor due its reading is fluctuating
        false_motion_reading = (PRECISION / 2) / RECOMMENDED_CYCLE_PERIOD

        return (self.speed() <= false_motion_reading and self.speed() >= -false_motion_reading)


"""
if __name__ == '__main__':
    try:
        while True:
            current_distance = proximity_sensor.distance()
            print ("Current measured Distance = " + str(current_distance) + "cm")
            time.sleep(1)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurements manually stopped")
        GPIO.cleanup()
"""