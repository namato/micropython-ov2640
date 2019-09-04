from ov2640_constants import *
from ov2640_lores_constants import *
from ov2640_hires_constants import *
import machine
import time
import ubinascii
import uos
import gc
import network
import socket
import os
machine.freq(240000000)
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect('TG1672G22','TG1672G0A4022') 
print('waiting....')
server_address=("192.168.0.10",int("5005"))
class ov2640(object):
    def __init__(self, sclpin=22, sdapin=21, cspin=15, resolution=OV2640_320x240_JPEG):
        self.sdapin=sdapin
        self.sclpin=sclpin
        self.cspin=cspin
        self.standby = False
        self.hspi = machine.SPI(1, baudrate=80000000, polarity=0, phase=0,bits=8,sck=machine.Pin(14), mosi=machine.Pin(13), miso=machine.Pin(12))
        self.i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21), freq=1000000)
        self.hspi.init(baudrate=8000000)
        self.cspin = machine.Pin(15, machine.Pin.OUT)
        self.cspin.on()
        addrs = self.i2c.scan()
        print('ov2640_init: devices detected on on i2c:')
        self.i2c.writeto_mem(SENSORADDR, 0xff, b'\x01')
        self.i2c.writeto_mem(SENSORADDR, 0x12, b'\x80')
        time.sleep_ms(60)
        cam_write_register_set(self.i2c, SENSORADDR, OV2640_JPEG_INIT)
        cam_write_register_set(self.i2c, SENSORADDR, OV2640_YUV422)
        cam_write_register_set(self.i2c, SENSORADDR, OV2640_JPEG)
        self.i2c.writeto_mem(SENSORADDR, 0xff, b'\x01')
        self.i2c.writeto_mem(SENSORADDR, 0x15, b'\x00')
        cam_write_register_set(self.i2c, SENSORADDR, resolution)
        cam_spi_write(b'\x00', b'\x55', self.hspi, self.cspin)
        res = cam_spi_read(b'\x00', self.hspi, self.cspin)
        print("ov2640 init:  register test return bytes %s" % ubinascii.hexlify(res))
        if (res == b'\x55'):
            print("ov2640_init: register test successful")
        else:
            print("ov2640_init: register test failed!")
        self.i2c.writeto_mem(SENSORADDR, 0xff, b'\x01')
        parta = self.i2c.readfrom_mem(SENSORADDR, 0x0a, 1)
        partb = self.i2c.readfrom_mem(SENSORADDR, 0x0b, 1)
        if ((parta != b'\x26') or (partb != b'\x42')):
            print("ov2640_init: device type does not appear to be ov2640, bytes: %s/%s" % \
                    (ubinascii.hexlify(parta), ubinascii.hexlify(partb)))
        else:
            print("ov2640_init: device type looks correct, bytes: %s/%s" % \
                    (ubinascii.hexlify(parta), ubinascii.hexlify(partb)))
    def capture_to_file(self, fn, overwrite):
        cam_spi_write(b'\x04', b'\x01', self.hspi, self.cspin)
        cam_spi_write(b'\x01', b'\x00', self.hspi, self.cspin)
        cam_spi_write(b'\x04', b'\x02', self.hspi, self.cspin)
        res = cam_spi_read(b'\x41', self.hspi, self.cspin)
        cnt = 0
        while True:
            res = cam_spi_read(b'\x41', self.hspi, self.cspin)
            mask = b'\x08'
            if (res[0] & mask[0]):
                break
            cnt += 1
        b1 = cam_spi_read(b'\x44', self.hspi, self.cspin)
        b2 = cam_spi_read(b'\x43', self.hspi, self.cspin)
        b3 = cam_spi_read(b'\x42', self.hspi, self.cspin)
        val = b1[0] << 16 | b2[0] << 8 | b3[0] 
        print("ov2640_capture: %d bytes in fifo" % val)
        gc.collect()
        bytebuf = [ 0, 0 ]
        picbuf = [ b'\x00' ] * PICBUFSIZE
        l = 0
        bp = 0
        if (overwrite == True):
            try:
                uos.remove(fn)
            except OSError:
                pass
        while ((bytebuf[0] != b'\xd9') or (bytebuf[1] != b'\xff')):
            bytebuf[1] = bytebuf[0]
            if (bp > (len(picbuf) - 1)):
                appendbuf(fn, picbuf, bp)
                bp = 0    
            bytebuf[0] = cam_spi_read(b'\x3c', self.hspi, self.cspin)
            l += 1
            picbuf[bp] = bytebuf[0]
            bp += 1
        if (bp > 0):
            appendbuf(fn, picbuf, bp)
        return (l)
    def standby(self):
        self.i2c.writeto_mem(SENSORADDR, 0xff, b'\x01')
        self.i2c.writeto_mem(SENSORADDR, 0x09, b'\x10')
        self.standby = True
    def wake(self):
        self.i2c.writeto_mem(SENSORADDR, 0xff, b'\x01')
        self.i2c.writeto_mem(SENSORADDR, 0x09, b'\x00')
        self.standby = False
def cam_write_register_set(i, addr, set):
    for el in set:
        raddr = el[0]
        val = bytes([el[1]])
        if (raddr == 0xff and val == b'\xff'):
            return
        i.writeto_mem(addr, raddr, val)
def appendbuf(fn, picbuf, howmany):
    try:
        f = open(fn, 'ab')
        c = 1
        print("writing")
        for by in picbuf:
            if (c > howmany):
                break
            c += 1
            f.write(bytes([by[0]]))
        f.close()
        print("done writing")
    except OSError:
        print("error writing file")
def cam_spi_write(address, value, hspi, cspin):
    cspin.off()
    modebit = b'\x80'
    d = bytes([address[0] | modebit[0], value[0]])
    hspi.write(d)
    cspin.on()
def cam_spi_read(address, hspi, cspin):
    cspin.off()
    maskbits = b'\x7f'
    wbuf = bytes([address[0] & maskbits[0]])
    hspi.write(wbuf)
    buf = hspi.read(1)
    cspin.on()
    return (buf)


