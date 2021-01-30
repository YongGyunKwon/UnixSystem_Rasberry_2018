import Adafruit_DHT
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.IN) 

count = 0
i=0
GPIO.setmode(GPIO.BCM)
sensor = Adafruit_DHT.DHT22
RED_LED = 18
GREEN_LED = 23
GPIO.setup(RED_LED, GPIO.OUT)
GPIO.setup(GREEN_LED, GPIO.OUT)
pin = 4

GPIO.output(GREEN_LED, GPIO.HIGH)
try: 
    while True:

        inputValue = GPIO.input(14)

        if (inputValue == True): 
            count = count +1 
            
            if (count%2==1):
                print("Start !") 
                for i in range(1,4):
                    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
                    from datetime import datetime
                    now = datetime.now()
                    if humidity is not None and temperature is not None:
                        print('%s/%s/%s %s:%s:%s'%(now.year, now.month, now.day, now.hour, now.minute, now.second))
                        print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
                        if(humidity>60 or humidity<40):
                            print("Warning")
                            GPIO.output(RED_LED, GPIO.HIGH)
                            time.sleep(1)
                        else:
                            print("Normal")
                            GPIO.output(RED_LED, GPIO.LOW)
                            time.sleep(1)
                    else:
                        print('print(Failed to get reading. Try again!)')
                        time.sleep(2)
                    i=i+1
                    if (i==4):
                        print('end !')
except KeyboardInterrupt:
    print("done")
    GPIO.cleanup()