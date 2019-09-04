import ov2640
import gc
import time
import sys
import network
import socket
import os
import ubinascii
import machine
machine.freq(240000000)
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect('TG1672G22','TG1672G0A4022') 
print('waiting....')
server_address=("192.168.0.10",int("5005"))
FNAME = 'image.jpg'
def main():
    try:
        print(gc.mem_free())
        clen = cam.capture_to_file(FNAME, True)
        print("captured image is %d bytes" % clen)
    
    except KeyboardInterrupt:
        print("exiting...")
        sys.exit(0)
def trx():
  f = open('image.jpg','rb')
  data=f.read()
  f.close()
  s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1) 
  s.connect(server_address)
  s.sendall(data)
  rdata=s.recvfrom(1024)
  print("Recieved Message")
  s.close()

if __name__ == '__main__':
  print("initializing camera")
  cam = ov2640.ov2640(resolution=ov2640.OV2640_320x240_JPEG)
  #cam = ov2640.ov2640(resolution=ov2640.OV2640_1024x768_JPEG)
  while True:
      main()
      trx()

