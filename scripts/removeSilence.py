# Requires FFMPEG
import sys
from pydub import AudioSegment
import subprocess
import os


def detectSilence(sound, silenceThreshold=-30.0, chunkSize=10):
  trimMs = 0  # ms
  while sound[trimMs: trimMs + chunkSize].dBFS < silenceThreshold:
    trimMs += chunkSize
  return trimMs


subprocess.call([
    "ffmpeg", "-i",
    f"{sys.argv[1]}",
    "input.wav"
])

sound = AudioSegment.from_file("input.wav", format="wav")

startTrim = detectSilence(sound)
endTrim = detectSilence(sound.reverse())

duration = len(sound)
trimmedSound = sound[startTrim: duration - endTrim]

trimmedSound.export("output.wav", format="wav")

AudioSegment.from_wav("output.wav").export(sys.argv[2], format="mp3")

os.remove("input.wav")
os.remove("output.wav")
