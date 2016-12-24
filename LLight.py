import requests
import time
import RPi.GPIO as GPIO
import threading
from neotest import *

# LED strip configuration:
LED_COUNT      = 12
LED_PIN        = 18
LED_FREQ_HZ    = 800000
LED_DMA        = 5
LED_BRIGHTNESS = 255
LED_INVERT     = False

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
strip.begin()

# LLight server stores the state that both lamps should share and modify
url = 'https://homes.cs.washington.edu/~jpaberc/LLight/llight.php'

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

swtch = 4
light = 17

GPIO.setup(swtch, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(light, GPIO.OUT)

prev_swtch_state = GPIO.LOW

def setState( state ) :
  r = requests.post(url+'/post', data={'state':state});

  return 

def getState() :
  global t
  r = requests.get(url)
  if (r.text == "ON"):
    GPIO.output(light, GPIO.HIGH)
    fill(strip)
  else:
    GPIO.output(light, GPIO.LOW)
    clear(strip)

  threading.Timer(5.0, getState).start()
  return

while True:
  
  swtch_state = GPIO.input(swtch)
  if (swtch_state != prev_swtch_state):
    if (swtch_state == GPIO.HIGH):    
      setState("ON")
      getState()

    else:
      setState("OFF")
      getState()
  prev_swtch_state = swtch_state
