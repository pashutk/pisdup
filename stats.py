import time
import subprocess

from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
from adafruit_ssd1306 import SSD1306_I2C

i2c = busio.I2C(SCL, SDA)
disp = SSD1306_I2C(128, 64, i2c, addr=0x3c, reset=None)
disp.fill(0)
disp.show()
width = disp.width
height = disp.height
# print(width)
# print(height)
image = Image.new("1", (width, height))
draw = ImageDraw.Draw(image)
draw.rectangle((0, 0, width, height), outline=0, fill=0)
# draw.rectangle((0, 0, 20, 20), outline=0, fill=255)

disp.image(image)
disp.show()

i = 0
while True:
    if i > width - 2:
        i = 0
    i = i + 1
    # disp.fill(0)
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    # draw.rectangle((i, 0, i + 2, height), outline=0, fill=255)
    draw.line([i, 0, i, height], fill=255, width=1)
    disp.image(image)
    disp.show()
    # time.sleep(.001)
