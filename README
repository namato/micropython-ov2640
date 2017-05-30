
# MicroPython class for OV2640 Camera

This is a basic interface to the [ArduCAM OV2640](http://www.arducam.com/camera-modules/2mp-ov2640/) under MicroPython for the ESP8266.  I wrote this because I could not find any good camera interfaces with MicroPython on the ESP8266.

Using this class you can:
* Initiate still pictures up to 1600x1200 resolution
* Read them from the camera
* Save them to flash on the ESP8266

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

First upload the module 'ov2640.py' into the root filesystem on the ESP8266 board you are using.

Then initialize and capture still frames using code like this:

```
import ov2640
cam = ov2640.ov2640()
path = cam.capture_to_file("/image.jpg")
```
You can then retrieve the image off of the board, upload it to a server via a REST API, etc. 
