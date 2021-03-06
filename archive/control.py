import time
import RPi.GPIO as GPIO
from timeit import default_timer as timer
import logging


class fcControl():

    trigger_pin = 14
    
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trigger_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        

    def light_on(self):
        self.light.on()
    def light_off(self):
        self.light.off()


    def cleanup(self):
        logging.info("Cleaning up GPIO")
        GPIO.cleanup()

 










class stepperControl:
    
    #initialise pins
    dir_pin = 18
    ms1_pin = 22
    ms2_pin = 23
    sleep_pin = 27
    reset_pin = 15
    pulse_pin = 17
    
    pulse_freq = 1000     # fastest stepper motor 17HD can go without skipping pulses etc
    #stepper motor control pins
    dir_fwd = False
    half_pulse =.5/pulse_freq
    steps_per_rev = 400 # 1 rev at quickest setting, where MS1 & MS2 = Low
    
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.dir_pin, GPIO.OUT)
        GPIO.setup(self.pulse_pin, GPIO.OUT)
        GPIO.setup(self.ms1_pin, GPIO.OUT)
        GPIO.setup(self.ms2_pin, GPIO.OUT)
        GPIO.setup(self.sleep_pin, GPIO.OUT)
        GPIO.setup(self.reset_pin, GPIO.OUT)
        GPIO.output(self.dir_pin, self.dir_fwd)
        GPIO.output(self.pulse_pin, False)
        GPIO.output(self.ms1_pin, False)
        GPIO.output(self.ms2_pin, False)
        GPIO.output(self.sleep_pin, False)
        GPIO.output(self.reset_pin, True)
        #self.pwm = GPIO.PWM(self.pulse_pin, self.pulse_freq)

    def wake(self):
        GPIO.output(self.sleep_pin, True)
        logging.debug("motor waking")
        time.sleep(.1)

    def sleep(self):
        GPIO.output(self.sleep_pin, False)
        logging.debug("motor sleeping")
        time.sleep(.1)
        

    def fwdFrame(self, num=1, speed=100):
        self.wake()
        logging.debug("fwdFrame "+str(num))
        self.windFrame(num)
        self.sleep()

    def windFrame(self, num=1, speed=100):
        pin=self.pulse_pin  #directly accessing for speed
        hp=self.half_pulse*speed/100
        for i in range (0,int(self.steps_per_rev*num)):
            GPIO.output(pin, True) #used instead of variable for speed
            time.sleep(hp) #again, directly entring num for speed
            GPIO.output(pin, False) #used instead of variable for speed
            time.sleep(hp)        
 
    def revFrame(self, num=1, speed=100):  #winds back one more than necessary, then forward to properly frame
        logging.debug("revFrame "+str(num))
        self.wake()
        GPIO.output(self.dir_pin, not self.dir_fwd)
        self.windFrame(num)
        GPIO.output(self.dir_pin, self.dir_fwd)
        self.sleep()


