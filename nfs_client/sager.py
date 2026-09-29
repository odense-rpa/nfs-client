"""Sagssøgning i NFS // Case search in NFS.

Port af Blue Prism handlingen "Hent sager" fra objektet "Netforvaltning Sundhed (Chrome)",
som bruges af processen "Lægeerklæringer - Betaling af statusattester".
"""

import re
import time
from datetime import date

from playwright.sync_api import Frame, Page, TimeoutError

from nfs_client.selectors import SagerSelectors as ss
from nfs_client.session import NFSSession

# kolonner i sagstabellen i den rækkefølge NFS viser dem
# // columns in the case table in the order NFS shows them
KOLONNER = [
    "Blanketnavn",
    "Ansvar",
    "Afdeling",
    "Borger",
    "Modtager",
    "Cpr",
    "Oprettelsesdato",
    "Besvaret af attestudsteder",
    "Status",
]
DATO_KOLONNER = {"Oprettelsesdato", "Besvaret af attestudsteder"}

POLL_MS = 100


def _dansk_dato(tekst: str) -> date | None:
    # dd-mm-yyyy (også . eller /) // dd-mm-yyyy (also . or /)
    match = re.fullmatch(r"(\d{1,2})[-./](\d{1,2})[-./](\d{4})", tekst.strip())
    if not match:
        return None
    dag, maaned, aar = (int(x) for x in match.groups())
    try:
        return date(aar, maaned, dag)
    except ValueError:
        return None


def _parse_raekker(raekker: list[list[str]]) -> list[dict]:
    """Omsætter tabelrækker (celletekster) til sager. Headerrækken bruges til at finde
    kolonnerne; uden header bruges rækkefølgen."""
    raekker = [[" ".join(celle.split()) for celle in raekke] for raekke in raekker]
    if not raekker:
        return []

    header = raekker[0]
    if header and header[0] == KOLONNER[0]:
        data = raekker[1:]
        indeks = {
            navn: header.index(navn) if navn in header else i
            for i, navn in enumerate(KOLONNER)
        }
    else:
        data = raekker
        indeks = {navn: i for i, navn in enumerate(KOLONNER)}

    sager = []
    for raekke in data:
        # pager- og andre korte rækker springes over // skip pager and other short rows
        if len(raekke) <= max(indeks.values()):
            continue
        sager.append(
            {
                navn: _dansk_dato(raekke[i]) if navn in DATO_KOLONNER else raekke[i]
                for navn, i in indeks.items()
            }
        )
    return sager


class SagerClient:
    """Sagshandlinger i NFS // Case actions in NFS.

    Oprettes af NFSClient og tilgås som nfs.sager.
    """

    def __init__(self, session: NFSSession):
        self._session = session

    def _sagsside(self, timeout: float = 30_000) -> Page | Frame:
        """Går til "Søg sager" og returnerer siden eller den frame, der har cpr-feltet."""
        page = self._session.gaa_til(ss.SAGSARKIV_STI)
        deadline = time.monotonic() + timeout / 1000
        while time.monotonic() < deadline:
            for omraade in [page, *page.frames]:
                if omraade.locator(ss.CPR).count() > 0:
                    return omraade
            page.wait_for_timeout(POLL_MS)
        raise TimeoutError("Cpr kom ikke frem")

    def _vent_paa_resultat(self, omraade: Page | Frame, timeout: float) -> bool:
        """Venter på resultatet. Returnerer False hvis der ingen sager er."""
        deadline = time.monotonic() + timeout / 1000
        while time.monotonic() < deadline:
            if omraade.locator(ss.INGEN_SAGER).count() > 0:
                return False
            if omraade.locator(f"{ss.SAGSTABEL} tr").count() > 1:
                return True
            self._session.page.wait_for_timeout(POLL_MS)
        raise TimeoutError("Sagstabel fandtes ikke")

    @staticmethod
    def _laes_tabel(omraade: Page | Frame) -> list[list[str]]:
        return omraade.locator(ss.SAGSTABEL).first.evaluate(
            "t => Array.from(t.rows).map("
            "r => Array.from(r.cells).map(c => c.innerText.trim()))"
        )

    def hent_sager(self, cpr: str) -> list[dict]:
        """Henter alle sager på en borger.

        Returnerer én dict pr. sag med nøglerne Blanketnavn, Ansvar, Afdeling, Borger,
        Modtager, Cpr, Oprettelsesdato, Besvaret af attestudsteder og Status. Datoerne er
        date eller None.
        """
        cpr = (cpr or "").replace("-", "").strip()
        if not re.fullmatch(r"\d{10}", cpr):
            raise ValueError("Cpr skal være 10 cifre")

        omraade = self._sagsside()
        omraade.locator(ss.CPR).fill(cpr)
        omraade.locator(ss.SAGSBEHANDLER).select_option(label=ss.ALLE_SAGSBEHANDLERE)

        # søgningen laver en fuld postback // the search does a full postback
        with omraade.expect_navigation():
            omraade.locator(ss.SOEG).click()

        if not self._vent_paa_resultat(omraade, 15_000):
            return []

        # læs alle sider, hvis tabellen har en pager // read all pages if there is a pager
        sager = []
        side = 1
        while True:
            sager += _parse_raekker(self._laes_tabel(omraade))
            naeste = omraade.locator(f'{ss.SAGSTABEL} a[href*="Page${side + 1}"]')
            if naeste.count() == 0:
                return sager
            with omraade.expect_navigation():
                naeste.first.click()
            side += 1
