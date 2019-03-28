
redLED = 15
greenLED = 13
blueLED = 11

GPIO.setmode(GPIO.BOARD)
GPIO.setup(redLED, GPIO.OUT)
GPIO.setup(greenLED, GPIO.OUT)
GPIO.setup(blueLED, GPIO.OUT)


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
