from pathlib import Path


def getFileNameWithoutExtension(fileName):
  return Path(fileName).stem
