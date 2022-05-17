from PIL import ImageGrab
from datetime import datetime
import sys

args = sys.argv[1:]
fileName = f"{datetime.today().strftime('%Y-%m-%d')}.png"

if (len(args) == 1):
  fileName = f"{args[0]}.png"

im = ImageGrab.grabclipboard()
im.save(fileName, "PNG")
