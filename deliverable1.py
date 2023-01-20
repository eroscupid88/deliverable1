import time
import RPi.GPIO as GPIO
# set pins GPIO
lightPins = (12,13,16) # green and red and blue
buttonPin = 11
sensorOutputPin = 40
light_state = 0
def setup():
    

    print("Set Up Phase")
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(sensorOutputPin,GPIO.IN,pull_up_down=GPIO.PUD_UP)
    GPIO.setup(lightPins,GPIO.OUT)
    GPIO.setup(buttonPin,GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(buttonPin, GPIO.BOTH, callback=pressButton,bouncetime = 100)
 #   GPIO.add_event_detect(sensorOutputPin,GPIO.BOTH,callback=sensorDetect,bouncetime = 100)
    GPIO.output(lightPins, GPIO.HIGH)
def blinkLight(state):
    global light_state
    if ((state == 0 and light_state == 0)or (state == 0 and light_state == 3)):
        GPIO.output(13,GPIO.LOW)
        GPIO.output(12,GPIO.HIGH)
        GPIO.output(16, GPIO.HIGH)
        light_state = 1
        print('light_state: %s'%light_state)
        return light_state
    if (state == 0 and light_state ==1):
        GPIO.output(12,GPIO.LOW)
        GPIO.output(13,GPIO.HIGH)
        GPIO.output(16, GPIO.HIGH)
        light_state = 2
        print('light_state: %s'%light_state)
        return light_state
    if (state== 0 and light_state ==2):
        GPIO.output(16,GPIO.LOW)
        GPIO.output(13,GPIO.HIGH)
        GPIO.output(12, GPIO.HIGH)
        light_state = 3
        print('light_state: %s'%light_state)
        return light_state
    if (state==0 and light_state == 3):
        GPIO.output(16,GPIO.LOW)
        GPIO.output(13,GPIO.LOW)
        GPIO.output(12, GPIO.LOW)
        light_state = 0
        print('light_state: %s'%light_state)
        return light_state

def onLight(state):
    if(state == 0):
        GPIO.output(13,GPIO.LOW)
        GPIO.output(12,GPIO.LOW)
        GPIO.output(16, GPIO.LOW)
    else:
        GPIO.output(13,GPIO.HIGH)
        GPIO.output(12,GPIO.HIGH)
        GPIO.output(16, GPIO.HIGH)
 
def pressButton(channel):
    print("button has been pressed")
    blinkLight(GPIO.input(buttonPin))

def sensorDetect(channel):
    print("Motion has been detected")
    onLight(GPIO.input(sensorOutputPin))
def loop():
    while(True):
        global light_state
        if (light_state == 3 and GPIO.input(sensorOutputPin) == 0):
            print("motion sensor is  detected")
            GPIO.output(13,GPIO.LOW)
            GPIO.output(12,GPIO.LOW)
            GPIO.output(16, GPIO.LOW)
        if (light_state == 3 and GPIO.input(sensorOutputPin) == 1):
            GPIO.output(13,GPIO.HIGH)
            GPIO.output(12,GPIO.HIGH)
            GPIO.output(16, GPIO.HIGH)           
        if (light_state == 0 ):
            GPIO.output(13,GPIO.HIGH)
            GPIO.output(12,GPIO.HIGH)
            GPIO.output(16, GPIO.HIGH)
        time.sleep(1)
def destroy():
    GPIO.output(lightPins,GPIO.HIGH)
    GPIO.cleanup()
if __name__ == "__main__":
    
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
