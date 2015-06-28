#!/usr/bin/env python3
"""
Pixellize
Generates a "pixellated" copy of IMAGEFILE.

Usage:
  pixellize.py [--length=L] [--pixels=P] IMAGEFILE
  pixellize.py -h | --help

Options:
  -h --help     Show this screen.
  --length=L    Lenght of the longest edge [default: 288].
  --pixels=P    Number of pixels to appear on the longest edge [default: 72].
"""
from docopt import docopt
from os.path import splitext
from PIL import Image
try:
    from schema import Schema, And, Or, Use, SchemaError
except ImportError:
    exit("This example requires that `schema` data-validation library"
         " is installed: \n    pip install schema\n"
         "https://github.com/halst/schema")


def level_image(image, minv=0, maxv=255, gamma=1.0):
    """
    Levels the brightness of image (a PIL.Image instance)
    All values ≤ minv will become 0
    All values ≥ maxv will become 255
    gamma controls the curve for all values between minv and maxv
    """

    source_mode = image.mode
    source = image.convert("HSV").split()
    h, s, v = 0, 1, 2

    def new_level(value):
        if value <= minv: return 0.0
        if value >= maxv: return 1.0
        new_value = ((value - minv) / (maxv - minv)) ** (1.0 / gamma)
        return int(new_value * 255.0)

    source[v].point(new_level)  # was lambda i: new_level(i)
    return Image.merge("HSV", source).convert(source_mode)


def scaled_size(factor, size):
    """
    Return a tuple (new_width, new_height) where both values are obtained from
    the size (width, heigth) rescaled by the same factor.
    """

    return tuple(int(dim * factor) for dim in size)


def pixellize(image,
              max_pixels=72,
              rescale=4.0,
              ncols=20,
              minv=14,
              maxv=181,
              gamma=1.51):
    """
    Generates a "pixellated" copy of `image` (a PIL.Image instance).
    It does it by 
      - adjusting its levels (`minv`, `maxv`) and `gamma` via the function level_image,
      - converting it to Idexed Mode with adaptive `ncols` colors (to avoid antialiasing)
      - scaling it down so that it has `max_pixels` pixels
      - rescaling it up by a factor of `rescale`
    """

    new_image = level_image(image, minv, maxv, gamma)
    if new_image.mode != "RGB":
        new_image = new_image.convert("RGB")
    new_image = new_image.convert("P", palette=Image.ADAPTIVE, colors=ncols)

    # scale factor is computed using % = max_new_size / max_size
    # and used to rescale the size of the image
    new_size = scaled_size(max_pixels / max(image.size), image.size)
    new_image = new_image.resize(new_size)
    final_size = scaled_size(rescale, new_image.size)
    return new_image.resize(final_size)


if __name__ == "__main__":
    args = docopt(__doc__, version="Pixellize 0.2")
    schema = Schema({
        "--help": Or(None, And(Use(bool))),
        "IMAGEFILE": Use(str, error="<imagefile> should be present"),
        "--length": Or(None, And(Use(int), lambda l: l > 0),
                       error="--length=L should be a positive integer (L>0)"),
        "--pixels": Or(None, And(Use(int), lambda p: p > 0),
                       error="--pixel=P should be a positive integer")
    })
    try:
        args = schema.validate(args)
    except SchemaError as e:
        exit(e)

    image_file = args["IMAGEFILE"]
    maxlen = args.get("--length", None)
    pixels = args.get("--pixels", 72)
    new_image_file = "-pix".join(splitext(image_file))
    print("Creating the pixellated", new_image_file, "from", image_file)

    with Image.open(image_file) as im:
        factor = maxlen / pixels if maxlen != None else 4.0
        uniform_size = scaled_size(1600 / max(im.size), im.size)
        pixellated = pixellize(im.resize(uniform_size),
                               rescale=factor,
                               max_pixels=pixels)
        pixellated.convert("RGB").save(new_image_file)
