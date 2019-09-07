from PIL import Image
from glob import glob
from os import *

for files in glob("*.jpg"):
    file, ext = path.splitext(files)
    im = Image.open(files)
    imr = im.resize((1366, 765))
    imr.save(file + "_resized.jpg", "JPEG")