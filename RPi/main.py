# importing all driver modules
import proximity_sensor_driver
import image_processor
import micro_servo_driver
import lcd_driver
import led_driver
import pi_cam_driver

import time


# module constants
def UNPROCESSED_IMG_NAME():
    return "vehicle_backside.jpg"

def PROCESSED_IMG_NAME():
    return "black_and_white.jpg"


def survey_vehicles():
    # declaring and initializing device drivers
    proximity_sensor_1 = proximity_sensor_driver.proximity_sensor(20, 21)
    lcd_1 = lcd_driver.lcd()
    led_set_1 = led_driver.led_set(13, 19, 26)
    micro_servo_1 = micro_servo_driver.micro_servo(16, 50, 20, 1, 1.5, 2)

    while True:
        if proximity_sensor_1.distance() <= 0.8 and proximity_sensor_1.is_stationary():
            pi_cam_driver.capture_image(UNPROCESSED_IMG_NAME)
            image_processor.grayscale_and_binarize(UNPROCESSED_IMG_NAME, PROCESSED_IMG_NAME, 128)
            vehicle_plate_number = image_processor.OCR(PROCESSED_IMG_NAME)
            
            if image_processor.is_registered(vehicle_plate_number):
                if not(image_processor.has_payed(vehicle_plate_number)):
                    led_set_1.turn_yellow_on
                    lcd_1.backlight(1)
                    lcd_1.lcd_display_string("Payment failed. E-wallet balance is insufficient, please recharge.")

                    # check every second if e-wallet has been recharged
                    while not(image_processor.has_payed(vehicle_plate_number)):
                        time.sleep(1)

                    led_set_1.turn_yellow_off
                    lcd_1.lcd_clear
                
                micro_servo_1.open_barrier()
                led_set_1.turn_green_on
                lcd_1.backlight(1)
                lcd_1.lcd_display_string("Payment successful.")

                # wait until vehicle leaves toll station
                while proximity_sensor_1.distance() < 3:
                    time.sleep(proximity_sensor_driver.RECOMMENDED_CYCLE_PERIOD)
                micro_servo_1.close_barrier()
                
                led_set_1.turn_green_off
                lcd_1.backlight(0)
                lcd_1.lcd_clear


            else:
                led_set_1.turn_red_on
                lcd_1.backlight(1)
                lcd_1.lcd_display_string("Vehicle is unregistered.")

                input("Has vehicle been checked? Press enter to continue.")

                micro_servo_1.open_barrier()
                # wait until vehicle leaves toll station
                while proximity_sensor_1.distance() < 3:
                    time.sleep(proximity_sensor_driver.RECOMMENDED_CYCLE_PERIOD)
                micro_servo_1.close_barrier()

                led_set_1.turn_red_off
                lcd_1.backlight(0)
                lcd_1.lcd_clear


        else:
            time.sleep(proximity_sensor_driver.RECOMMENDED_CYCLE_PERIOD)
