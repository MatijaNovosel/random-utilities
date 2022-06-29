import os
import ffmpeg
import sys


def compressVideo(videoFullPath, outputFileName, targetSize):
  minAudioBitrate = 32000
  maxAudioBitrate = 256000

  probe = ffmpeg.probe(videoFullPath)
  duration = float(probe['format']['duration'])
  audioBitrate = float(next(
      (s for s in probe['streams'] if s['codec_type'] == 'audio'), None)['bit_rate'])
  targetTotalBitrate = (targetSize * 1024 * 8) / (1.073741824 * duration)

  if 10 * audioBitrate > targetTotalBitrate:
    audioBitrate = targetTotalBitrate / 10
    if audioBitrate < minAudioBitrate < targetTotalBitrate:
      audioBitrate = minAudioBitrate
    elif audioBitrate > maxAudioBitrate:
      audioBitrate = maxAudioBitrate

  videoBitrate = targetTotalBitrate - audioBitrate

  i = ffmpeg.input(videoFullPath)
  ffmpeg.output(i, os.devnull,
                **{'c:v': 'libx264', 'b:v': videoBitrate, 'pass': 1, 'f': 'mp4'}
                ).overwrite_output().run()
  ffmpeg.output(i, outputFileName,
                **{'c:v': 'libx264', 'b:v': videoBitrate, 'pass': 2, 'c:a': 'aac', 'b:a': audioBitrate}
                ).overwrite_output().run()


# Input file, output file, size in MB
compressVideo(sys.argv[1], sys.argv[2], int(sys.argv[3]) * 1000)
