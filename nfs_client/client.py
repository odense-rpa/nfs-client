import httpx

from playwright.sync_api import (
    sync_playwright,
    Playwright,
    Page,
    Error as PlaywrightError,
)

class NFSClient:
    def __init__(self, base_url: str, username: str, password: str):
        self.base_url = base_url
        self.username = username
        self.password = password
        self._playwright: Playwright = sync_playwright().start()
        self._browser = self._playwright.chromium.launch(
            headless=False,            
        )
        self._context = self._browser.new_context(
            viewport={"width": 1920, "height": 1080},
            accept_downloads=False,
            ignore_https_errors=True,
            locale="da-DK",
        )
        self._page: Page = (
            self._context.pages[0] if self._context.pages else self._context.new_page()
        )

        self.login()

    def login(self):
        self._page.goto(self._base_url)
        asoidjasd = ""

    def luk_side(self):
        pass

    def hent_bruger(self):
        pass

    def slet_bruger(self):
        pass