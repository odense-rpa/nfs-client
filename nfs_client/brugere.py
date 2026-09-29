"""Brugeradministration i NFS // User administration in NFS."""

from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import Locator, Page, expect

from nfs_client.selectors import NFSSelectors
from nfs_client.session import NFSSession


class BrugerClient:
    """Brugerhandlinger i NFS // User actions in NFS.

    Oprettes af NFSClient og tilgås som nfs.brugere.
    """

    def __init__(self, session: NFSSession, email: str = ""):
        self._session = session
        self.email = email or ""

    @property
    def _page(self) -> Page:
        return self._session.page

    def soeg_bruger(self, email: str) -> Locator:
        """Søger en kommunal bruger på e-mail og returnerer resultattabellen."""
        email = (email or self.email or "").strip()
        if not email:
            raise ValueError("A valid email must be provided to soeg_bruger")

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
        try:
            results_table = frame_content_locator.locator(
                NFSSelectors.LISTE_OVER_BRUGERE
            )
            results_table.wait_for(state="visible", timeout=60000)
            result_row = results_table.locator(f"tbody > tr:has-text('{email}')")
            result_row.first.wait_for(state="visible", timeout=60000)
        except PlaywrightError:
            raise ValueError(f"Ingen bruger fundet med email: {email}")
        return results_table

    def naviger_til_bruger(self, email: str):
        results_table = self.soeg_bruger(email)

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

        # Workflow: 1) første popup accepteres altid, 2) anden popup (advarsel) accepteres
        # og dens besked rejses som ValueError.
        dialog_messages: list[str] = []

        def _capture_delete_dialog(dialog):
            dialog_messages.append(dialog.message)
            dialog.accept()

        self._page.on("dialog", _capture_delete_dialog)
        try:
            delete_btn.click()

            # Første popup forventes altid.
            for _ in range(70):
                if dialog_messages:
                    break
                self._page.wait_for_timeout(100)

            if not dialog_messages:
                raise RuntimeError(
                    "Forventet bekræftelsesdialog ved sletning blev ikke vist"
                )

            # Anden popup vises kun ved advarselsscenariet (typisk forsinket 3-5 sek.).
            for _ in range(60):
                if len(dialog_messages) >= 2:
                    break
                self._page.wait_for_timeout(100)

            if len(dialog_messages) >= 2:
                raise ValueError(dialog_messages[1])
        finally:
            self._page.remove_listener("dialog", _capture_delete_dialog)

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

        self._page.click(NFSSelectors.FORSIDE_LINK)
        self._page.wait_for_timeout(5000)
