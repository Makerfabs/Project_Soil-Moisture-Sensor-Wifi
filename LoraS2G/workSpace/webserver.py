#webserver.py
import network
import webrepl
import time
from machine import Pin
try:
  import usocket as socket
except:
  import socket

AUTH_OPEN = 0
AUTH_WEP = 1
AUTH_WPA_PSK = 2
AUTH_WPA2_PSK = 3
AUTH_WPA_WPA2_PSK = 4

SSID = "Makerfabs"      #Modify here with SSID
PASSWORD = "20160704"   #Modify here with PWD
led = Pin(5, Pin.OUT)
ip = "ip get wrong"

def web_page(adc):
  status = "UNKNOW"
  if adc > 800:
    soil_word = """<p style="background:blue" width:250px>TOO DRY</p>"""
  elif adc > 600:
    soil_word = """<p style="background:green" width:250px>VERY GOOD!</p>"""
  elif adc > 200:
    soil_word = """<p style="background:yellow" width:250px>TOO WET</p>"""
  else :
    soil_word = """<p style="background:red" width:250px>ERROR DEGREE</p>"""
  
  html ="""
  <html>
    <head><meta name="viewport" content="width=device-width, initial-scale=1"><meta http-equiv="refresh" content="30"/></head>
    <body>
      <img src="https://makerfabs.com/image/cache/logo11-190x63.png" />
      <h1>Lora Soil Sensor</h1>
      <h2>Soil Sensor status:""" + str(adc) + """</h2>
      """ + soil_word + """
    </body>
  </html>
  """
  return html

def do_connect(ssid,psw):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    s = wlan.config("mac")
    mac = ('%02x:%02x:%02x:%02x:%02x:%02x').upper() %(s[0],s[1],s[2],s[3],s[4],s[5])
    print("Local MAC:"+mac) #get mac 
    wlan.connect(ssid, psw)
    if not wlan.isconnected():
        print('connecting to network...' + ssid)
        wlan.connect(ssid, psw)

    start = time.ticks_ms() # get millisecond counter
    while not wlan.isconnected():
        time.sleep(1) # sleep for 1 second
        if time.ticks_ms()-start > 20000:
            print("connect timeout!")
            break

    if wlan.isconnected():
        print('network config:', wlan.ifconfig())
        global ip
        ip = str(wlan.ifconfig())
    return wlan

def connect():
 do_connect(SSID,PASSWORD)
 global ip
 return ip
