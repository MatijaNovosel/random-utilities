import sys
from bs4 import BeautifulSoup
import requests
import asyncio
from pyppeteer import launch
import urllib.request
import subprocess
import os


def constructUrl(param, id: str):
    return f"https://v.redd.it/{id}/DASH_{param}.mp4"


possibleQualities = [220, 240, 360, 480, 720]
url = sys.argv[1]


async def main():
    validVideoUrls = []

    browser = await launch()
    page = await browser.newPage()
    await page.goto(url)

    response = await page.content()
    soup = BeautifulSoup(response, "html.parser")
    anchor = soup.select_one("source")

    videoId = anchor["src"].split("/")[3]

    for quality in possibleQualities:
        videoUrl = constructUrl(quality, videoId)
        resp = requests.get(videoUrl)
        if (resp.status_code != 403):
            validVideoUrls.append(videoUrl)

    if len(validVideoUrls) != 0:
        audioUrl = constructUrl("audio", videoId)
        urllib.request.urlretrieve(audioUrl, "audio.mp4")
        urllib.request.urlretrieve(validVideoUrls[-1], "redditVid.mp4")

        subprocess.call([
            "ffmpeg", "-i", "redditVid.mp4", "-i", "audio.mp4", "-shortest",
            "output.mp4"
        ])

        os.remove("redditVid.mp4")
        os.remove("audio.mp4")

    await browser.close()


asyncio.get_event_loop().run_until_complete(main())
