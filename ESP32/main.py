import ov2640
import gc
import time
import sys

FNAME = 'image2.jpg'

def main():
    try:
        print("initializing camera")
        #cam = ov2640.ov2640(resolution=ov2640.OV2640_320x240_JPEG)
        cam = ov2640.ov2640(resolution=ov2640.OV2640_1024x768_JPEG)
        print(gc.mem_free())
    
        clen = cam.capture_to_file(FNAME, True)
        print("captured image is %d bytes" % clen)
        print("image is saved to %s" % FNAME)
    
        time.sleep(10)
        sys.exit(0)
    
    except KeyboardInterrupt:
        print("exiting...")
        sys.exit(0)


if __name__ == '__main__':
    main()
