
# Dexclock

A e-paper clock that also shows dexcom blood sugar readings for diabetics.

![](https://github.com/sKrible45/dexclock/blob/main/pictures/tutorial5.jpg)

## Parts List
- [Raspberry Pi Pico W](https://shop.pimoroni.com/products/raspberry-pi-pico-w?variant=40059369619539)

- [E-paper Display](https://shop.pimoroni.com/products/adafruit-2-13-hd-tri-color-eink-epaper-display-featherwing-250x122-rw-panel-with-ssd1680?variant=32321752924243)

- [Buttons](https://www.adafruit.com/product/367)

- [Neopixel Leds](https://kitronik.co.uk/products/35129-zip-strip?_pos=3&_sid=e352da038&_ss=r)

- The stl file for the case is in the repo.
## Libraries

 - [Pydexcom](https://github.com/gagebenne/pydexcom)
 - [Pydexcom on circuitpython](https://github.com/spovlot/circuitpython_pydexcom)
 - [circuitpython Libraries](https://circuitpython.org/libraries)


## Features

- Shows blood glocose levels from dexcom.
- Shows time from the internet

## Downsides

- It can only update the time and glocose every 3 minutes.

## Circuit Diagram

![](https://github.com/sKrible45/dexclock/blob/main/pictures/pinout.jpg)


## Building Instructions
First print out the stl files `Clock Case.stl` and `Clock Case Besel.stl` in the repo or use printing service like pcb-way.
Then put the rpi pico into the desegnated spot like in this image.(you may need to glue it.)

![](https://github.com/sKrible45/dexclock/blob/main/pictures/tutorial1.jpg)

Next solder 7 wires onto the points from this image or the pinout diagram.

![](https://github.com/sKrible45/dexclock/blob/main/pictures/tutorial.jpg)

Now solder the wires from the screen on to the rpi pico's pins as shown in the pinout image.

![](https://github.com/sKrible45/dexclock/blob/main/pictures/tutorial2.jpg)

Then solder the button to `GND` and `GPIO1` on the `pico` and solder neopixels to `VCC` , `GND` and `A1` on the pico like in the pinout image.

![](https://github.com/sKrible45/dexclock/blob/main/pictures/tutorial4.jpg)

Push the button into the whole on the top of the case and glue it there.(you may need to file down the whole to make it fit).
After that, glue the neopixel board to the stiking out plane at the top of the case faceing down.
Then glue the screen board onto the mounting points in this image. 

![](https://github.com/sKrible45/dexclock/blob/main/pictures/screen%20mounting.png)

Now glue the besel onto the screen like in this image.

![](https://github.com/sKrible45/dexclock/blob/main/pictures/tutorial5.jpg)

And your done, now you can do the software.

## Software Instructions

First download the circuit python uf2 from here https://circuitpython.org/board/raspberry_pi_pico_w/

Next plug your raspberry pi pico into our computer; it should come up as a usb drive called `rpi-rpi2`.
Drag the uf2 file that you downloaded onto the rpi pico drive.

There should be a drive that appears caled `CIRCUITPY`.

Then download the repo and unzip it.
Go into the "Main" folder (inside the repo you downloaded)and copy the contense onto the `CIRCUITPY` drive.(replace code.py with main.py.)

Open code.py and replace `"dexcom password"` on line `26` with your dexcom account's password
and with `"dexcom username"` on line `27` replace it with your dexcom account's username.
Replace `"wifi password"` on line `29` with your wifi's password and `"wifi ssid"` with your wifi's name on line `28`.
Replace this section `Europe/London` on line `31` with the one for your timezone; heres a link to help with that http://worldtimeapi.org/timezones.
And your done it should all be finished and ready to go.(exept if you are in the us then follow the next instruction.)


## An extra thing for people in the US.
Delete `ous = True` on line `105`.
And your done it should all be finished and ready to go.

