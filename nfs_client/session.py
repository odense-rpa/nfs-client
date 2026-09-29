"""Browsersession til Netforvaltning Sundhed // Browser session for NFS.

NFSSession ejer browseren og login, som områdeklienterne (sager, brugere) deler.
"""

from urllib.parse import urljoin

from playwright.sync_api import BrowserContext, Page, Playwright, sync_playwright


class NFSSession:
    """Én browser og ét login, delt af alle områdeklienter."""

    def __init__(
        self,
        base_url: str,
        username: str,
        password: str,
        headless: bool | None = None,
    ):
        self.base_url = base_url or "about:blank"
        self.username = username or ""
        self.password = password or ""
        self.headless = True if headless is None else headless
        self._playwright: Playwright | None = None
        self._browser = None
        self._context: BrowserContext | None = None
        self._page: Page | None = None

        # ryd op hvis login fejler, så Playwright ikke efterlades kørende
        # // clean up if login fails so Playwright is not left running
        try:
            self._login()
        except Exception:
            self.close()
            raise

    @property
    def page(self) -> Page:
        if self._page is None:
            raise RuntimeError("NFS-sessionen er lukket")
        return self._page

    @property
    def context(self) -> BrowserContext:
        if self._context is None:
            raise RuntimeError("NFS-sessionen er lukket")
        return self._context

    def _ensure_browser(self) -> None:
        if self._page is not None:
            return

        self._playwright = sync_playwright().start()
        self._browser = self._playwright.chromium.launch(headless=self.headless)
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

    def _login(self) -> None:
        self._ensure_browser()
        self.page.goto(self.base_url, wait_until="domcontentloaded")
        self.page.wait_for_timeout(5000)

    def gaa_til(self, sti: str) -> Page:
        """Går til en side i NFS, fx "/Authority/CaseArchive.aspx"."""
        self.page.goto(urljoin(self.base_url, sti), wait_until="domcontentloaded")
        return self.page

    def close(self) -> None:
        if self._context is not None:
            self._context.close()
            self._context = None

        if self._browser is not None:
            self._browser.close()
            self._browser = None

        if self._playwright is not None:
            self._playwright.stop()
            self._playwright = None

        self._page = None
