import subprocess
import os
import sys

cwd = os.getcwd()

subprocess.call([
    "youtube-dl",
    "-o",
    f"{cwd}/downloads/%(title)s-%(id)s.%(ext)s",
    f"{sys.argv[1]}"
])
