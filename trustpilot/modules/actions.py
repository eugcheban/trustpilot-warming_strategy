
"""
Playwright-based parser for search results:
1. Save results of search request to DB (just urls of products)
2. Get data for each product by its url and save it to DB (for the test - just for the first product)
"""

import asyncio
from sqlite3 import IntegrityError

from playwright.async_api import async_playwright
from playwright.async_api import Error as PlaywrightError
from asgiref.sync import sync_to_async
from load_django import *
from user.models import User
from pathlib import Path
import dotenv
import os
import requests
import hashlib

BASE_DIR = Path(__file__).resolve().parent.parent

dotenv.load_dotenv(os.path.join(BASE_DIR, '.env'))


def get_token():
    url = "https://api.multilogin.com/user/signin"
    payload = {
        "email": os.getenv("USERNAME"),
        "password": hashlib.md5(os.getenv("PASSWORD").encode()).hexdigest()
    }
    r = requests.post(url, json=payload)
    if r.status_code != 200:
        print(f"Error getting token: {r.text}")
        return None
    return r.json().get("data", {}).get("token")


def start_browser(token):
    url = f"https://launcher.mlx.yt:45001/api/v2/profile/f/{os.getenv('FOLDER_ID')}/p/{os.getenv('PROFILE_ID')}/start"
    params = {"automation_type": "playwright"}
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.get(url, headers=headers, params=params, verify=False)
    data = res.json()

    port = data.get('value') or data.get('data', {}).get('port')
    return port


# Register account on Trustpilot wich has status "New" on DB
async def account_registraton(page):
    # login_button
    await page.goto("https://www.trustpilot.com/")
    await page.wait_for_timeout(300)
    await page.locator('a[name="navigation-login-desktop"]').click()


async def main():
    token = get_token()
    if not token:
        raise ValueError("Failed to get Multilogin token")

    port = start_browser(token)
    if not port:
        raise ValueError("Failed to get browser port from Multilogin")

    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(f"http://127.0.0.1:{port}")
        context = browser.contexts[0]
        page = context.pages[0] if context.pages else await context.new_page()

        await account_registraton(page)


if __name__ == "__main__":
    asyncio.run(main())
    