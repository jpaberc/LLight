import requests
import time
import RPi.GPIO as GPIO
import threading
import unicornhat as unicorn


GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# LLight server stores the state that both lamps should share and modify
url = 'https://ssqpad.hopto.org:9180'

id = 0

def trigger(channel):
      state = setState()
      toggle(state)
      print "toggled state to ", state


GPIO.add_event_detect(4, GPIO.RISING, callback=trigger, bouncetime=900)

def toggle ( status ) :
      if status != None :
            if status['state'] == 0:
                  light_off()
            elif status['state'] == 1:
                  print "(", status['color']['r'], ",",status['color']['g'],",", status['color']['b'],")"
                  light_on(status['color']['r'], status['color']['g'], status['color']['b'])

def setState ( ) :
      print "posting state"
      r = None
      try :
            response = requests.post(url+"?id="+str(id), verify=False)
      except :
            print "post failed"
      else :
            r = response.json()
      finally :
            return r

def getState ( ) :
      print "requesting status"
      r = None
      try :
            response = requests.get(url, verify=False)
      except :
            print "get failed"
      else :
            r = response.json()
      finally:
            return r

def light_on ( r,g,b ) :
      unicorn.set_layout(unicorn.AUTO)
      unicorn.rotation(0)
      unicorn.brightness(0.8)
      width,height=unicorn.get_shape()

      for y in range(height):
            for x in range(width):
                  unicorn.set_pixel(x,y,r,g,b)
      unicorn.show()

def light_off ( ) :
      unicorn.set_layout(unicorn.AUTO)
      unicorn.rotation(0)
      unicorn.brightness(0.0)
      width,height=unicorn.get_shape()

      for y in range(height):
            for x in range(width):
                  unicorn.set_pixel(x,y,0,0,0)

      unicorn.show()
      
def getLoop ( ) :
      toggle(getState())
      t = threading.Timer(5.0, getLoop)
      t.daemon = True
      t.start()

getLoop()

while True:
      if False:
            print
