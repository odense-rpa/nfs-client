import httpx
from nfs_client.selectors import NFSSelectors

from playwright.sync_api import (
    sync_playwright,
    Playwright,
    Page,
    Frame,
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


    def _find_frame_with_selector(self, frame: Frame, selector: str) -> Frame | None:
        try:
            if frame.locator(selector).count() > 0:
                return frame
        except PlaywrightError:
            pass

        for child in frame.child_frames:
            found = self._find_frame_with_selector(child, selector)
            if found is not None:
                return found

        return None


    def fremsøg_bruger(self, email: str | None = None):
        self._ensure_browser()

        if self._page is None:
            return None

        email = (email or self.email or "").strip()
        if not email:
            raise ValueError("A valid email must be provided to fremsøg_bruger")

        #Navigering
        self._page.hover(NFSSelectors.TILPASNING)
        self._page.click(NFSSelectors.KOMMUNENS_BRUGERE)

        #Håndtering af iframe
        self._page.wait_for_selector("iframe#frameset", timeout=30000)
        frameset_frame = self._page.frame(name="frameset")
        if frameset_frame is None:
            raise RuntimeError("iframe#frameset not found")

        frameset_frame.wait_for_load_state("domcontentloaded", timeout=30000)

        target_frame = self._find_frame_with_selector(
            frameset_frame, NFSSelectors.EMAIL_SØGEFELT
        )
        if target_frame is None:
            raise RuntimeError(
                f"Could not find selector {NFSSelectors.EMAIL_SØGEFELT} inside iframe#frameset"
            )

        email_field = target_frame.locator(NFSSelectors.EMAIL_SØGEFELT)
        email_field.wait_for(timeout=30000)

        #Søgning
        email_field.fill(email)
        target_frame.locator(NFSSelectors.EMAIL_SØGEKNAP).click()

        # Vent på at resultater er klar i iframe-rammen
        rows = target_frame.locator(NFSSelectors.BRUGER_RÆKKE)
        rows.first.wait_for(state="visible")

        target_email = email.lower()
        count = rows.count()

        matched_rows = []
        for i in range(count):
            row = rows.nth(i)
            email_cell = row.locator(NFSSelectors.EMAIL_KOLONNE)
            rolle_cell = row.locator(NFSSelectors.ROLLE_KOLONNE)
            if email_cell.count() == 0 or rolle_cell.count() == 0:
                continue

            email_text = email_cell.inner_text().strip().lower()
            rolle_text = rolle_cell.inner_text().strip().lower()
            if email_text != target_email or rolle_text == "admin":
                continue

            matched_rows.append(row)

        # Hvis match fundet, klik på detaljer
        if len(matched_rows) == 1:
            matched_rows[0].locator("td:nth-child(5) a").click()
            return self._page
        if len(matched_rows) == 0:
            raise ValueError(f"Ingen bruger fundet med email: {email}")

        raise ValueError(f"Flere brugere fundet med email: {email}")


    def slet_bruger(self, email: str):
        bruger_side = self.fremsøg_bruger(email)
        
        if bruger_side is None:
            raise ValueError(f"Bruger med email {email} kunne ikke findes for sletning")
        
        # TODO: Sletnings logik