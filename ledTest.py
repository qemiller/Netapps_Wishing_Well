import RPi.GPIO as GPIO
import time

redLED = 15
greenLED = 13
blueLED = 11

channelList = [redLED,greenLED,blueLED]
GPIO.setmode(GPIO.BOARD)
GPIO.setup(channelList, GPIO.OUT)


def waitingForTweet():
    GPIO.output(redLED, True)
    GPIO.output(blueLED, True)
    GPIO.output(greenLED, True)
    time.sleep(2)
    GPIO.output(redLED, False)
    GPIO.output(blueLED, False)
    GPIO.output(greenLED, False)
    

def receivedPublish():
    GPIO.output(redLED,True)
    time.sleep(2)
    GPIO.output(redLED,False)


def receivedConsume():
    GPIO.output(greenLED,True)
    time.sleep(2)
    GPIO.output(greenLED,False)

receivedConsume()
GPIO.cleanup()
