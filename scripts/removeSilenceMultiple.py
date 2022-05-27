import os
import sys
from pydub import AudioSegment
from zipfile import ZipFile
import subprocess


def detectSilence(sound, silenceThreshold=-30.0, chunkSize=10):
  trimMs = 0  # ms
  while sound[trimMs: trimMs + chunkSize].dBFS < silenceThreshold:
    trimMs += chunkSize
  return trimMs


def listFiles(path):
  files = []
  for name in os.listdir(path):
    if os.path.isfile(os.path.join(path, name)):
      files.append(name)
  return files


files = listFiles(sys.argv[1])
zipObj = ZipFile("noSilence.zip", "w")

for file in files:
  print(file)

  subprocess.call(['ffmpeg', '-i', f"{sys.argv[1]}/{file}",
                   'input.wav'])

  sound = AudioSegment.from_file("input.wav", format="wav")

  startTrim = detectSilence(sound)
  endTrim = detectSilence(sound.reverse())

  duration = len(sound)
  trimmedSound = sound[startTrim: duration - endTrim]

  trimmedSound.export("output.wav", format="wav")
  AudioSegment.from_wav("output.wav").export(file, format="mp3")

  zipObj.write(file)
  os.remove(file)
  os.remove("input.wav")
  os.remove("output.wav")

zipObj.close()
