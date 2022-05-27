import sys
from pydub import AudioSegment


def detectSilence(sound, silenceThreshold=-20.0, chunkSize=10):
  trimMs = 0  # ms
  while sound[trimMs: trimMs + chunkSize].dBFS < silenceThreshold:
    trimMs += chunkSize
  return trimMs


AudioSegment.from_wav(
    sys.argv[1]).export("input.wav", format="wav")

sound = AudioSegment.from_file("input.wav", format="wav")

startTrim = detectSilence(sound)
endTrim = detectSilence(sound.reverse())

duration = len(sound)
trimmedSound = sound[startTrim: duration - endTrim]

trimmedSound.export("output.wav", format="wav")

AudioSegment.from_wav("output.wav").export(sys.argv[1], format="mp3")
