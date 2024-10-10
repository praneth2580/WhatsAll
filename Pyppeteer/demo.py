import asyncio
import os

PYPPETEER_CHROMIUM_REVISION = '1267552'
os.environ['PYPPETEER_CHROMIUM_REVISION'] = PYPPETEER_CHROMIUM_REVISION

from pyppeteer import launch

async def main():
    browser = await launch()
    page = await browser.newPage()
    await page.goto('https://quotes.toscrape.com/')

    ## Get Title
    title_html = await page.querySelector('h1')
    title = await title_html.getProperty("textContent")
    print('title', title)

    await browser.close()

asyncio.get_event_loop().run_until_complete(main())

