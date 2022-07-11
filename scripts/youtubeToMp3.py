import subprocess
import sys

subprocess.call(
    ["youtube-dl", "--extract-audio", "--audio-format", "mp3", sys.argv[1]])
