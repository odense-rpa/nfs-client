import httpx
from nfs_client.selectors import NFSSelectors
from playwright.sync_api import (
    expect,
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

    def _søg_bruger(self, email: str):
        self._ensure_browser()

        if self._page is None:
            return None

        email = (email or self.email or "").strip()
        if not email:
            raise ValueError("A valid email must be provided to fremsøg_bruger")

        # navigering
        self._page.hover(NFSSelectors.TILPASNING)
        self._page.click(NFSSelectors.KOMMUNENS_BRUGERE)

        # håndtering af iframe
        self._page.wait_for_selector(NFSSelectors.IFRAME, timeout=60000)
        frameset_locator = self._page.frame_locator(NFSSelectors.IFRAME)
        frame_content_locator = frameset_locator.frame_locator(
            NFSSelectors.IFRAME_CONTENT
        )
        frame_content_locator.locator(NFSSelectors.FORM).wait_for(
            state="visible", timeout=60000
        )

        # vent på email_søgefelt selector
        email_field = frame_content_locator.locator(NFSSelectors.EMAIL_SØGEFELT)
        email_field.wait_for(state="visible", timeout=60000)

        # søgning
        email_field.fill(email)
        frame_content_locator.locator(NFSSelectors.EMAIL_SØGEKNAP).click()

        # vent på at resultater er klar i iframe-rammen
        results_table = frame_content_locator.locator(NFSSelectors.LISTE_OVER_BRUGERE)
        results_table.wait_for(state="visible", timeout=60000)
        result_row = results_table.locator(f"tbody > tr:has-text('{email}')")
        result_row.first.wait_for(state="visible", timeout=60000)
        return results_table

    def naviger_til_bruger(self, email: str):
        results_table = self._søg_bruger(email)

        # match email med resultat
        target_email = email.lower()
        rows = results_table.locator("tbody > tr")
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

        # Hvis match fundet, returner resultat eller klik på detaljer
        if len(matched_rows) == 1:
            matched_rows[0].locator(NFSSelectors.DETALJER_FOR_BRUGER).click()
            return matched_rows[0]
        if len(matched_rows) == 0:
            raise ValueError(f"Ingen bruger fundet med email: {email}")

        raise ValueError(f"Flere brugere fundet med email: {email}")

    def slet_bruger(self, email: str):
        bruger_side = self.naviger_til_bruger(email)

        if bruger_side is None:
            raise ValueError(f"Bruger med email {email} kunne ikke findes for sletning")

        # håndtering af iframe
        self._page.wait_for_selector(NFSSelectors.IFRAME, timeout=60000)
        frameset_locator = self._page.frame_locator(NFSSelectors.IFRAME)
        frame_content_locator = frameset_locator.frame_locator(
            NFSSelectors.IFRAME_CONTENT
        )

        frame_content_locator.locator(NFSSelectors.FORM).wait_for(
            state="visible", timeout=60000
        )

        delete_btn = frame_content_locator.locator(NFSSelectors.SLET_BRUGER_KNAP)
        delete_btn.wait_for(state="visible", timeout=60000)

        # håndter fail-safe & slet klik
        for frame in self._page.frames:
            frame.evaluate("window.confirm = () => true")

        delete_btn.click()

        # Genstart søgningen for at validere, at brugeren virkelig er væk
        search_field = frame_content_locator.locator(NFSSelectors.EMAIL_SØGEFELT)
        search_field.wait_for(state="visible", timeout=60000)
        search_field.fill(email)
        frame_content_locator.locator(NFSSelectors.EMAIL_SØGEKNAP).click()

        result_locator = frame_content_locator.locator(
            NFSSelectors.RESULTAT_I_LISTE_OVER_BRUGER
        )

        try:
            expect(result_locator).to_have_count(0, timeout=15000)

        except PlaywrightError:
            raise RuntimeError(f"Bruger med email {email} blev ikke slettet korrekt")
