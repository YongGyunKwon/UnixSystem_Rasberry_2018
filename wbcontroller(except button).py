from bottle import get, post, run
import RPi.GPIO as GPIO
import Adafruit_DHT
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.IN) 
inputValue=GPIO.input(14)

GPIO.setmode(GPIO.BCM)
dht22 = Adafruit_DHT.DHT22
RED_LED = 18
GREEN_LED=23
pin=4

count=0
i=0

GPIO.setup(RED_LED, GPIO.OUT)
GPIO.output(RED_LED, False)
GPIO.setup(GREEN_LED, GPIO.OUT)
GPIO.output(GREEN_LED, True)

from datetime import datetime
now=datetime.now()

def update_led(led_value):
    GPIO.output(RED_LED, led_value)

def update_gled(gled_value):
    GPIO.output(GREEN_LED, gled_value)


        
def make_html(gled_value=False,led_value=False, temperature=0, humidity=0):
    led_status = "On"
    gled_status="On"
    if not led_value:
        led_status = "Off"
    if not gled_value:
        gled_status = "Off"
    response = """
    
    <html>
      <head>
        <title>Humidity Sensor</title>
      </head>
      <body>
        <h1>Humidity SenSor</h1>
        <form action="/sensor_led" method="post">
          <br/>
          <h2>GREEND LED        : %s</h2>
          <h2>Time: %s - %s - %s        %s :%s :%s</h2>
          <h2>Temperature: %0.1f</h2>
          <h2>Humidity   : %0.1f</h2>
          <h2>RED LED        : %s</h2>
          <br/>
          <input style="height:80px;width:160px;font-size:20px" type='submit' value='Button'/>
        </form> 
      </body>
    </html>
    """ % (gled_status,now.year,now.month,now.day,now.hour,now.minute,now.second,temperature,humidity, led_status)
    return response

@get('/sensor_led')
def index():
    update_gled(False)
    update_led(False)
    return make_html()

@post('/sensor_led')
def sensor_led():
        for i in range(1,4):
            humidity, temperature = Adafruit_DHT.read_retry(dht22, pin)
            led_value = False
            gled_value= True
            if humidity <= 40 or humidity>=60:
                    led_value = True
            update_led(led_value)
            update_gled(gled_value)
            time.sleep(1)
            return make_html(gled_value,led_value, temperature, humidity)

run(host='0.0.0.0', port=8090)

GPIO.cleanup()
