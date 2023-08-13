
import time
import board
import displayio
import busio
import terminalio
import adafruit_ssd1680
from adafruit_display_text import label
import wifi
import ssl
import socketpool
import adafruit_requests as requests
from circuitpython_pydexcom.pydexcom import Dexcom
from adafruit_display_shapes.roundrect import RoundRect
from adafruit_display_shapes.circle import Circle
from rainbowio import colorwheel
import neopixel
from digitalio import DigitalInOut, Direction, Pull


BLACK = 0x000000
WHITE = 0xFFFFFF
RED = 0xFF0000

# set your credentials here.
dexcompass = "dexcom password"
dexcomuser = "dexcom user"
wifissid = "wifi ssid"
wifipass = "wifi password"
#time api link.
region = "Europe/London" 
timeurl = "http://worldtimeapi.org/api/timezone/" + region

#hyper above this number
highbg = 14.0

#hypo below this number.
lowbg = 4.0


#setup button and leds.
btn = DigitalInOut(board.GP1)
btn.direction = Direction.INPUT
btn.pull = Pull.UP
pixel_pin = board.A1
num_pixels = 5
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.3, auto_write=False)
bg = 0

#make a backround image.
background_bitmap = displayio.Bitmap(250, 122, 1)
palette = displayio.Palette(1)
palette[0] = WHITE

displayio.release_displays()

#set the SPI pins.
spi = busio.SPI(board.GP2,board.GP3,board.GP4)  # Uses SCK and MOSI
epd_cs = board.GP10
epd_dc = board.GP11

#init the display
display_bus = displayio.FourWire(
    spi, command=epd_dc, chip_select=epd_cs, baudrate=1000000
)
time.sleep(1)
display = adafruit_ssd1680.SSD1680(
    display_bus,
    colstart=8,
    width=250,
    height=122,
    highlight_color=0xFF0000,
    rotation=270
)


#########################################################################################################################################

# define the functions
def displayclear(): # clears the display
  global g
  g = displayio.Group()
  t = displayio.TileGrid(background_bitmap, pixel_shader=palette)
  g.append(t)
  display.show(g)


#########################################################################################################################################


def wificonect(): #conects to the network and inits dexcom
  for i in range(10):
    try:
      global wifissid
      global wifipass
      print("conecting to " + str(wifissid))
      wifi.radio.connect(wifissid,wifipass)
      print("conected to " + str(wifissid))
      print("My ip adress is " + str(wifi.radio.ipv4_address))
      global socket
      global requests
      socket = socketpool.SocketPool(wifi.radio)
      requests = requests.Session(socket, ssl.create_default_context())
      global dexcom
      dexcom = Dexcom(dexcomuser,dexcompass,request_session=requests,ous = True)
      break
    except:
      pass


#########################################################################################################################################


def DrawGragh():
  #draw high bg line and number.
  g.append(label.Label(terminalio.FONT, text=str(int(highbg)), color=RED, x=45, y=(180 - int(int(highbg) * 10)) // 2))
  g.append(RoundRect(x = 0,y = (((180 - int(int(highbg) * 10)) // 2) - ((180 - int(int(highbg) * 10)) // 2)) - 2,fill = RED,width = 42,height = ((180 - int(int(highbg) * 10)) // 2),r = 1))
  g.append(RoundRect(x = 0,y = ((180 - int(int(highbg) * 10)) // 2),fill = RED,width = 42,height = 1,r = 0))

  #draw low bg line and number.
  g.append(label.Label(terminalio.FONT, text=str(int(lowbg)), color=RED, x=45, y=(180 - int(int(lowbg) * 10)) // 2))
  g.append(RoundRect(x = 0,y = (180 - int(int(lowbg) * 10)) // 2,fill = RED,width = 42,height = 1,r = 0))
  g.append(RoundRect(x = 0,y = ((180 - int(int(lowbg) * 10)) // 2) + 2,fill = RED,width = 42,height = 85 - ((180 - int(int(lowbg) * 10)) // 2),r = 1))
  #draw graph.
  space = 45
  for bg in bgprev:
    space -= 6
    if hasattr(bg,"mmol_l"):
      print(bg.time, bg.mmol_l)
      g.append(Circle(space, (180 - int(bg.mmol_l * 10)) // 2, 2, fill=BLACK, outline=BLACK))


#########################################################################################################################################

def DrawHighGragh():
  g.append(RoundRect(x = 0,y = 0,fill = RED,width = 42,height = 85,r = 1))
  #draw high bg number and line.
  g.append(label.Label(terminalio.FONT, text=str(int(highbg)), color=BLACK, x=45, y=(220 - int(int(highbg) * 10)) // 2))
  g.append(RoundRect(x = 0,y = ((220 - int(int(highbg) * 10)) // 2),fill = BLACK,width = 42,height = 1,r = 0))
  #draw bg 22 line and number.
  g.append(label.Label(terminalio.FONT, text="22", color=BLACK, x=45, y=6))
  g.append(RoundRect(x = 0,y = 6,fill = BLACK,width = 42,height = 1,r = 0))
  #draw graph.
  space = 45
  for bg in bgprev:
    space -= 6
    if hasattr(bg,"mmol_l"):
      print(bg.time, bg.mmol_l)
      g.append(Circle(space, (220 - int(bg.mmol_l * 10)) // 2, 2, fill=BLACK, outline=BLACK))


#########################################################################################################################################

def DrawHud():
  #draw high bg line and number.
  g.append(label.Label(terminalio.FONT, text=str(int(highbg)), color=RED, x=45, y=(180 - int(int(highbg) * 10)) // 2))
  g.append(RoundRect(x = 0,y = (((180 - int(int(highbg) * 10)) // 2) - ((180 - int(int(highbg) * 10)) // 2)) - 2,fill = RED,width = 42,height = ((180 - int(int(highbg) * 10)) // 2),r = 1))
  g.append(RoundRect(x = 0,y = ((180 - int(int(highbg) * 10)) // 2),fill = RED,width = 42,height = 1,r = 0))

  #draw low bg line and number.
  g.append(label.Label(terminalio.FONT, text=str(int(lowbg)), color=RED, x=45, y=(180 - int(int(lowbg) * 10)) // 2))
  g.append(RoundRect(x = 0,y = (180 - int(int(lowbg) * 10)) // 2,fill = RED,width = 42,height = 1,r = 0))
  g.append(RoundRect(x = 0,y = ((180 - int(int(lowbg) * 10)) // 2) + 2,fill = RED,width = 42,height = 85 - ((180 - int(int(lowbg) * 10)) // 2),r = 1))


#########################################################################################################################################



def ledsleep():
  #time in seconds times 50.
  looptimes = 180 / 0.05
  for i in range(looptimes):
    if not btn.value:
      pixels.fill((50,50,50))
      pixels.show()
      time.sleep(4)
      pixels.fill((0,0,0))
      pixels.show()
    time.sleep(0.05)


#########################################################################################################################################


wificonect()


#########################################################################################################################################


while True:
  displayclear()

  if (wifi.radio.connected == False):
    wificonect()
  
  #get the dexcom glocose readings
  if (wifi.radio.connected == True):
    try:
      bg = dexcom.get_current_glucose_reading()   
      bgprev = dexcom.get_glucose_readings(max_count=8)
      if hasattr(bg,"mmol_l"):
        if (bg.mmol_l >= 18):
          DrawHighGragh()
        else:
          DrawGragh()
      else:
        DrawHud()
        bg = 0
    except:
      pass
    response = requests.get(timeurl)
    timeoutput = response.text
    strtime = timeoutput[72: -313]
    date = timeoutput[69: -319] + "/" + timeoutput[66: -322] + "/" + timeoutput[63: -325]
    numday = timeoutput[109: -280]
    strday = "Mon"
    if (numday == "1"):
      strday = "Mon"
    elif (numday == "2"):
      strday = "Tue"
    elif (numday == "3"):
      strday = "Wed"
    elif (numday == "4"):
      strday = "Thu"
    elif (numday == "5"):
      strday = "Fri"
    elif (numday == "6"):
      strday = "Sat"
    elif (numday == "7"):
      strday = "Sun"
    print(strday)
  else:
    bg = 0
    bgprev = 0
    strtime = "**:**"
    date = "**/**/**"


  # print glocose
  if hasattr(bg,"mmol_l"):
    if (bg.mmol_l <= lowbg or bg.mmol_l >= highbg):
      BGtext_area = label.Label(terminalio.FONT, text=str(bg.mmol_l), color=RED, x=0, y=110,scale=2)
    else:
      BGtext_area = label.Label(terminalio.FONT, text=str(bg.mmol_l), color=BLACK, x=0, y=110,scale=2)
    print(date,strtime,":",bg.mmol_l)
  else:
    BGtext_area = label.Label(terminalio.FONT, text="**.*", color=BLACK, x=0, y=110,scale=2)


  #print time and date values
  DAYtext_area = label.Label(terminalio.FONT, text=strday, color=BLACK, x=80, y=110,scale=2)
  DATEtext_area = label.Label(terminalio.FONT, text=date, color=BLACK, x=150, y=110,scale=2)
  TIMEtext_area = label.Label(terminalio.FONT, text=strtime, color=BLACK, x=60, y=45,scale=6)
  #show the line
  g.append(RoundRect(x = 0,y = 90,fill = BLACK,width = 250,height = 5,r = 2))
  # show the image and refesh
  g.append(BGtext_area)
  g.append(DAYtext_area)
  g.append(DATEtext_area)
  g.append(TIMEtext_area)
  display.refresh()
  ledsleep()