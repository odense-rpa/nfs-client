import httpx
from nfs_client.selectors import NSFSelectors

from playwright.sync_api import (
    sync_playwright,
    Playwright,
    Page,
    Error as PlaywrightError,
)

class NFSClient:
    def __init__(self, base_url: str, username: str, password: str, email: str = ""):
        self.base_url = base_url or "about:blank"
        self.username = username or ""
        self.password = password or ""
        self.email = email or ""
        self._playwright: Playwright | None = None
        self._browser = None
        self._context = None
        self._page: Page | None = None

    def _ensure_browser(self) -> None:
        if self._page is not None:
            return

        self._playwright = sync_playwright().start()
        self._browser = self._playwright.chromium.launch(headless=False)
        self._context = self._browser.new_context(
            viewport={"width": 1920, "height": 1080},
            accept_downloads=False,
            ignore_https_errors=True,
            locale="da-DK",
            http_credentials={"username": self.username, "password": self.password},
        )
        self._page = (
            self._context.pages[0] if self._context.pages else self._context.new_page()
        )

    def login(self):
        self._ensure_browser()
        if self._page is None:
            return None

        self._page.goto(self.base_url, wait_until="domcontentloaded")
        print(self._page.url)
        self._page.wait_for_timeout(5000)
        return self._page

    def close(self) -> None: 
        self._context.close()
        self._browser.close()
        self._playwright.stop()

    def fremsøg_bruger(self, email: str = ""):
        self._ensure_browser()

        if self._page is None:
            return None

        #Søgning
        self._page.hover(NSFSelectors.TILPASNING)
        self._page.click(NSFSelectors.KOMMUNENS_BRUGERE)
        self._page.fill(NSFSelectors.EMAIL_SØGEFELT, email)
        self._page.click(NSFSelectors.EMAIL_SØGEKNAP)

        # Vent på at resultater er klar
        rows = self._page.locator(NSFSelectors.BRUGER_RÆKKE)
        rows.first.wait_for(state="visible")


        # lokaliser den rigtige række baseret på email og klik på detaljer
        target_email = email.strip().lower()
    
        count = rows.count()

        for i in range(count):
            row = rows.nth(i)
    
            email_text = row.locator(NSFSelectors.EMAIL_KOLONNE).inner_text().strip().lower()
    
            if email_text == target_email:
                row.locator(NSFSelectors.DETALJER_FOR_BRUGERE).click()
                return self._page
    
        raise ValueError(f"Ingen bruger fundet med email: {email}")

    def slet_bruger(self):
        pass