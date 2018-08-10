import os
from tempfile import NamedTemporaryFile
from PIL import Image, ImageEnhance, ImageDraw, ImageFont
from pdfconduit.watermark.lib import FONT
from pdfconduit.utils import resource_path, bundle_dir


def img_opacity(image, opacity, tempdir=None, bw=True):
    """
    Reduce the opacity of a PNG image.

    Inspiration: http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/362879

    :param image: PNG image file
    :param opacity: float representing opacity percentage
    :param tempdir: Temporary directory
    :param bw: Set image to black and white
    :return: Path to modified PNG
    """
    # Validate parameters
    assert 0 <= opacity <= 1, 'Opacity must be a float between 0 and 1'
    assert os.path.isfile(image), 'Image is not a file'

    # Open image in RGBA mode if not already in RGBA
    im = Image.open(image)
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    else:
        im = im.copy()

    # Adjust opacity
    alpha = im.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    im.putalpha(alpha)
    if bw:
        im.convert('L')

    # Save modified image file
    dst = NamedTemporaryFile(suffix='.png', dir=tempdir, delete=False)
    im.save(dst)
    return dst.name


class DrawPIL:
    def __init__(self, size=(792, 612), tempdir=None):
        # Create a black image
        self.img = Image.new('RGBA', size, color=(255, 255, 255, 0))  # 2200, 1700 for 200 DPI
        self.tempdir = tempdir

    def _centered_x(self, text, drawing, font):
        # Get img size
        page_width = self.img.size[0]
        text_width = drawing.textsize(text, font=font)[0]
        x = (page_width - text_width) / 2
        return x

    def _centered_y(self, size):
        # Get img size
        page_height = self.img.size[1]
        y = (page_height - size) / 2
        return y

    def _scale(self, img):
        im = img if isinstance(img, Image.Image) else Image.open(img)

        scale = min(float(self.img.size[0] / im.size[0]), float(self.img.size[1] / im.size[1]))

        im.thumbnail((int(im.size[0] * scale), int(im.size[1] * scale)))

        return im if isinstance(img, Image.Image) else self.save(img=im)

    def draw_text(self, text, x='center', y=140, font=FONT, size=40, opacity=0.1):
        # Set drawing context
        d = ImageDraw.Draw(self.img)

        # Set a font
        fnt = ImageFont.truetype(font, int(size * 1.25))

        # Check if x is set to 'center'
        if 'center' in str(x).lower():
            x = self._centered_x(text, d, fnt)

        # Check if y is set to 'center'
        if 'center' in str(y).lower():
            y = self._centered_y(size)

        # Draw text to image
        d.text((x, y), text, font=fnt, fill=(0, 0, 0, int(255 / (opacity * 100))))

    def draw_img(self, img, x=0, y=0, opacity=1.0):
        scaled = self._scale(img)

        # scaled = im.resize(target_width)
        opacity = Image.open(img_opacity(scaled, opacity, self.tempdir))

        self.img.paste(opacity, (x, y))

    def rotate(self, rotate):
        # Create transparent image that is the same size as self.img
        mask = Image.new('L', self.img.size, 255)

        # Rotate image and then scale image to fit self.img
        front = self._scale(self.img.rotate(rotate, expand=True))

        # Rotate mask
        self._scale(mask.rotate(rotate, expand=True))

        # Determine difference in size between mask and front
        x_margin = int((mask.size[0] - front.size[0]) / 2)

        # Create another new image
        rotated = Image.new('RGBA', self.img.size, color=(255, 255, 255, 0))

        # Paste front into new image and set x offset equal to half the difference of front and mask size
        rotated.paste(front, (x_margin, 0))
        self.img = rotated

    def save(self, destination=None, file_name='pil', img=None):
        img = self.img if not img else img
        fn = file_name.strip('.png') if '.png' in file_name else file_name
        if self.tempdir:
            tmpimg = NamedTemporaryFile(suffix='.png', dir=self.tempdir, delete=False)
            output = resource_path(tmpimg.name)
        elif destination:
            output = os.path.join(destination, fn + '.png')
        else:
            output = os.path.join(bundle_dir(), fn + '.png')

        # Save image file
        img.save(output)
        return output
