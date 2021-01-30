from bottle import get, post, run
import RPi.GPIO as GPIO
import Adafruit_DHT

GPIO.setmode(GPIO.BCM)

led_pin = 18

dht22 = Adafruit_DHT.DHT22
dht22_pin = 4

GPIO.setup(led_pin, GPIO.OUT)
GPIO.output(led_pin, False)

def update_led(led_value):
    GPIO.output(led_pin, led_value)

def make_html(led_value=False, temperature=0, humidity=0):
    led_status = "On"
    if not led_value:
        led_status = "Off"
    response = """
    <html>
      <head>
        <title>Sensing & LED Control</title>
      </head>
      <body>
        <h1>Sensing & LED Control</h1>
        <form action="/sensor_led" method="post">
          <br/>
          <h2>Temperature: %0.1f</h2>
          <h2>Humidity   : %0.1f</h2>
          <h2>LED        : %s</h2>
          <br/>
          <input style="height:80px;width:160px;font-size:20px" type='submit' value='Refresh'/>
        </form>
      </body>
    </html>
    """ % (temperature, humidity, led_status)
    return response

@get('/sensor_led')
def index():
    update_led(False)
    return make_html()

@post('/sensor_led')
def sensor_led():
    humidity, temperature = Adafruit_DHT.read_retry(dht22, dht22_pin)
    led_value = True
    if temperature <= 30:
        if humidity >= 50:
            led_value = False
    update_led(led_value)
    return make_html(led_value, temperature, humidity)

run(host='0.0.0.0', port=8080)

GPIO.cleanup()