import math
from PIL import Image, ImageDraw, ImageFont, ImageChops

def trim(im):

    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    bbox = diff.getbbox()

    if bbox:
        return im.crop(bbox)

class Shindanji ():

    def __init__ (self, width=64, height=64):

        self.dimensions = (width, height)

    def drawRadical (self, char, size=50, verbose=False):

        assert isinstance(char, str)

        W, H = (size, size)

        image = Image.new("RGBA", (W, H))

        draw = ImageDraw.Draw(image)

        font = ImageFont.truetype("data/arial_unicode.ttf", size)

        w, h = draw.textsize(char, font=font)
        draw.text(((W - w)/2, (H - h)/2 - size/10), char, fill=(0, 0, 0, 255), font=font)

        image = trim(image)

        dimensions = (3, 3) #[math.ceil(3*x/size) for x in image.size]

        if verbose:
            return image, dimensions

        else:
            return image

    def drawChar (self, data, size=50, _toplayer=True):

        assert isinstance(data, list)

        char = Image.new("RGBA", (size, size))

        for component in data:

            if isinstance(component["radical"], list):
                # Draw characters and run through iteratively
                radical = self.drawChar(component["radical"], size=size, _toplayer=False)
                dimensions = (3, 3)

            else:
                # {"radical": "", "positions": [[H], [W]]}
                radical, dimensions = self.drawRadical(component["radical"], size=size, verbose=True)

            # Squeeze dimensions if necessary
            positions = component["positions"]
            given_dimensions = [positions[0][1] - positions[0][0] + 1, positions[1][1] - positions[1][0] + 1]

            height_ratio = round(given_dimensions[0]/dimensions[0] * size)
            width_ratio = round(given_dimensions[1]/dimensions[1] * size)

            radical = radical.resize((height_ratio, width_ratio))
            draw_positions = [round((positions[0][0] - 1)/3 * size), round((positions[1][0] - 1)/3 * size)]

            char.paste(radical, draw_positions, radical)

        return trim(char)
