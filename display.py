from PIL import Image, ImageDraw, ImageFont
from config import Config, UI_OUT
if Config.UI_OUT is UI_OUT.SD11306:
    from adafruit_ssd1306 import SSD1306_I2C
    import busio
    from board import SCL, SDA

if Config.UI_OUT is UI_OUT.PYGAME:
    import pygame


class DisplayColor:
    BLACK = 0
    WHITE = 255


class Display:
    def __init__(self):
        self.image = Image.new(
            Config.DISPLAY_IMAGE_MODE, (Config.DISPLAY_WIDTH, Config.DISPLAY_HEIGHT))
        self.font = ImageFont.load_default()
        self.draw = ImageDraw.Draw(self.image)
        self.pygame_instance = None
        self.pygame_screen = None
        self.ssd1306 = None

        if Config.UI_OUT is UI_OUT.PYGAME:
            pygame.display.set_caption("PISDUP EMU")
            self.pygame_screen = pygame.display.set_mode(self.image.size)

        if Config.UI_OUT is UI_OUT.SD11306:
            self.ssd1306 = SSD1306_I2C(Config.DISPLAY_WIDTH, Config.DISPLAY_HEIGHT, busio.I2C(
                SCL, SDA), addr=Config.I2C_DISPLAY_ADDR, reset=None)
            self.ssd1306.fill(DisplayColor.BLACK)

    # Run this one to update image on screen
    def show(self):
        if Config.UI_OUT is UI_OUT.STATIC_IMAGE:
            self.image.show()
        elif Config.UI_OUT is UI_OUT.PYGAME:
            image = self.image.convert(Config.PYGAME_IMAGE_MODE)
            image_bytes = image.tobytes('raw', Config.PYGAME_IMAGE_MODE)
            surface = pygame.image.fromstring(
                image_bytes, image.size, image.mode).convert()
            self.pygame_screen.blit(surface, (0, 0))
            pygame.display.update()
        elif Config.UI_OUT is UI_OUT.SD11306:
            self.ssd1306.image(self.image)
            self.ssd1306.show()
        else:
            raise Exception("Unknown UI output")

    def use_draw(self, draw_fn, opt_clear_canvas=True):
        if opt_clear_canvas:
            self.draw.rectangle((0, 0, self.image.width,
                                 self.image.height), outline=0, fill=DisplayColor.BLACK)
        draw_fn(self.draw)

    def draw_white_text(self, pos, text):
        self.draw.text(
            pos, text, font=self.font, fill=DisplayColor.WHITE)

    def textsize(self, text):
        return self.draw.textsize(text, font=self.font)

    def image_paste(self, image, xy):
        x, y = xy
        w, h = image.size
        self.image.paste(image, xy + (x + w, y + h))

    def draw_icons(self):
        y = 32
        pad = 10
        self.draw.multiline_text(
            (pad, y - 1), "Need\ndis:", fill=DisplayColor.WHITE, font=self.font, spacing=2)

        sd = Image.open('icon_sd.png')
        hdd = Image.open('icon_hdd.png')
        w = self.image.width
        sdw = sd.width
        hddw = hdd.width
        hddx = w - pad - hddw
        sdx = hddx - pad - sdw
        self.image_paste(sd, (sdx, y))
        self.image_paste(hdd, (hddx, y))

    def draw_topbar_text(self, text):
        w, h = self.textsize(text)
        x = (self.image.width - w) // 2
        if x < 0:
            x = 0

        self.draw_white_text((x, 2), text)

    def draw_centered_text(self, text):
        w, h = self.textsize(text)
        x = (self.image.width - w) // 2
        y = (self.image.height - h) // 2

        self.draw_white_text((x, y), text)
