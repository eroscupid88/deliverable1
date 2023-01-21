import time
import RPi.GPIO as GPIO
# set pins GPIO
lightPins = (12,13,16) # 12: green ; 13: red ; 16: blue
buttonPin = 11 
sensorOutputPin = 40
light_state = 0
# initial set up function only call 1
def setup():
    print("Set Up Phase"
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(sensorOutputPin,GPIO.IN,pull_up_down=GPIO.PUD_UP)
    GPIO.setup(lightPins,GPIO.OUT)
    GPIO.setup(buttonPin,GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(buttonPin, GPIO.BOTH, callback=pressButton,bouncetime = 100)
    # setup output light turn off when high
    GPIO.output(lightPins, GPIO.HIGH)
    
# blinkLight function turn on differents light depend on the state system'
# param: state: 0 -> when button is pressed, 1 -> when button is not pressed
def blinkLight(state):
    global light_state
    # first state: RED LED on
    if ((state == 0 and light_state == 0)or (state == 0 and light_state == 3)):
        GPIO.output(13,GPIO.LOW)
        GPIO.output(12,GPIO.HIGH)
        GPIO.output(16, GPIO.HIGH)
        light_state = 1
        return light_state
    #second state: GREEN LED on
    if (state == 0 and light_state ==1):
        GPIO.output(12,GPIO.LOW)
        GPIO.output(13,GPIO.HIGH)
        GPIO.output(16, GPIO.HIGH)
        light_state = 2
        return light_state
    # third state: BLUE LED on
    if (state== 0 and light_state ==2):
        GPIO.output(16,GPIO.LOW)
        GPIO.output(13,GPIO.HIGH)
        GPIO.output(12, GPIO.HIGH)
        light_state = 3
        return light_state
    # forth state: ALL LED on (this state motion sensor is activated)
    if (state==0 and light_state == 3):
        GPIO.output(16,GPIO.LOW)
        GPIO.output(13,GPIO.LOW)
        GPIO.output(12, GPIO.LOW)
        light_state = 0
        return light_state
# onLight function call when sensor is activated
# params: state: 0 -> sensor detected motion; 1 -> sensor not detected motion
def onLight(state):
    if(state == 0):
        GPIO.output(13,GPIO.LOW)
        GPIO.output(12,GPIO.LOW)
        GPIO.output(16, GPIO.LOW)
    else:
        GPIO.output(13,GPIO.HIGH)
        GPIO.output(12,GPIO.HIGH)
        GPIO.output(16, GPIO.HIGH)
 
# callback function pressButton activate when button is pressed          
def pressButton(channel):
    print("button has been pressed")
    blinkLight(GPIO.input(buttonPin))
# when sensor is activated, seonsorDetect function is called
def sensorDetect(channel):
    print("Motion has been detected")
    onLight(GPIO.input(sensorOutputPin))
#main loop only run on state 4 
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
        # turn off all light when system state is 0
        if (light_state == 0 ):
            GPIO.output(13,GPIO.HIGH)
            GPIO.output(12,GPIO.HIGH)
            GPIO.output(16, GPIO.HIGH)
        time.sleep(1)
# destroy function is called when system is interrupted and clean up all preset
def destroy():
    GPIO.output(lightPins,GPIO.HIGH)
    GPIO.cleanup()
#initial setup          
if __name__ == "__main__":
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
