
# MicroPython class for OV2640 Camera

This is a basic interface to the [ArduCAM OV2640](http://www.arducam.com/camera-modules/2mp-ov2640/) under MicroPython for the ESP8266.  I wrote this because I could not find any good camera interfaces with MicroPython on the ESP8266.

Using this class you can:
* Initiate still pictures up to 1600x1200 resolution
* Read them from the camera
* Save them to flash on the ESP8266

After saving the image you can use other modules to post it to a REST API,
or save a (short) history of pictures on the flash for later retrieval.

## Usage - Hardware Setup

This particular camera has both an i2c and spi interface for setup and
getting data on/off the camera.  A good way to wire up the camera to
the ESP8266 is as follows (note Vcc and GND pins are not included here):

 Camera Pin | ESP8266 Pin  |
| --------- | ------------ |
| CS        | GPIO2        |
| MOSI      | GPIO13       |
| MISO      | GPIO12       |
| SCK       | GPIO14       |
| SDA       | GPIO4        |
| SCL       | GPIO5        |

## Usage - Software

First upload the module 'ov2640.py' into the root filesystem on the
ESP8266 board you are using.  The [ampy](https://github.com/adafruit/ampy)
tool from Adafruit is a useful tool for doing that.  Together with
[esptool](https://github.com/espressif/esptool), you can re-flash your
board and load the code here in one shot with these commands.

First download the latest MicroPython [image from here](http://micropython.org/download#esp8266).

```
sudo esptool.py --port /dev/ttyUSB0 erase_flash
sudo esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash --flash_size=detect 0 ~/Downloads/esp8266-20170526-v1.9.bin
git clone https://github.com/namato/micropython-ov2640
cd micropython-ov2640
sudo ampy -p /dev/ttyUSB0 put boot.py
sudo ampy -p /dev/ttyUSB0 put main.py
sudo ampy -p /dev/ttyUSB0 put ov2640_constants.py
sudo ampy -p /dev/ttyUSB0 put ov2640_hires_constants.py
sudo ampy -p /dev/ttyUSB0 put ov2640_lores_constants.py
sudo ampy -p /dev/ttyUSB0 put ov2640.py
```

Then initialize and capture still frames using code like this.  The included `main.py` contains an example.

```
import ov2640
cam = ov2640.ov2640()
nbytes = cam.capture_to_file("/image.jpg")
```
You can then retrieve the image off of the board, upload it to a server, etc.

A good way to retrieve files for testing/verification is
[rshell](https://github.com/dhylands/rshell).

```
sudo rshell -p /dev/ttyUSB0
Connecting to /dev/ttyUSB0 ...
Welcome to rshell. Use Control-D to exit.
/home/namato/micropython-ov2640> 
/home/namato/micropython-ov2640> cp /image2.jpg .
```

This will copy the newly created image locally for viewing.

## Credits

The original driver source from Arducam was instrumental in the creation of this pure
MicroPython version.

The overall project was inspired by
[esparducam](https://johan.kanflo.com/building-the-esparducam/), but
getting this to work doesn't require any SMD soldering. :)

