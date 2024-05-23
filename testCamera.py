from picamera2 import Picamera2, Preview
from libcamera import controls
import time, os

os.environ['XDG_RUNTIME_DIR'] = '/run/user/1000'
os.chmod(os.environ['XDG_RUNTIME_DIR'], 0o777)
os.environ['DISPLAY'] = ':0'
picam2 = Picamera2()


config = picam2.create_preview_configuration(main={"size": (1920, 1080)})
picam2.configure(config)
picam2.set_controls({"ColourGains": (1.85, 1.85)}) #Tuple of two floating point numbers between 0.0 and 32.0.
picam2.start_preview(Preview.QTGL)

picam2.start()
while True:
	time.sleep(1)
# picam2.capture("test.jpg")

picam2.close()

