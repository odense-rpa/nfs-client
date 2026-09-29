# nfs-client

Playwright-baseret Python-klient til Netforvaltning Sundhed (NFS, `nfs.kommuneinformation.dk`) — sagssøgning og brugeradministration via browserautomatisering.

> Denne klient er ikke officielt støttet eller godkendt af leverandøren bag NFS. Brug på eget ansvar.

## Nuværende funktionalitet

- Autentificering mod NFS-webapplikationen via HTTP basic auth og Chromium
- **Sager** (`nfs.sager`): hent alle sager på en borger (cpr) fra "Søg sager"
- **Brugere** (`nfs.brugere`): søg kommunale brugere på e-mail, gå til brugerens detaljeside
  (administratorroller filtreres fra) og slet brugeren med efterfølgende verifikation

## Installation

```bash
uv add git+https://github.com/odense-rpa/nfs-client
```

## Forudsætninger

- Python ≥ 3.13
- Playwright-browser: `uv run playwright install chromium`
- Adgang til NFS-webapplikationen med gyldige HTTP-loginoplysninger

## Brug

```python
from nfs_client import NFSClient

with NFSClient(
    base_url="https://nfs.kommuneinformation.dk",
    username="brugernavn",
    password="adgangskode",
) as nfs:
    sager = nfs.sager.hent_sager("0101011234")
    nfs.brugere.slet_bruger("bruger@kommune.dk")
```

### Sager (`nfs.sager`)

- `hent_sager(cpr)` — port af Blue Prism handlingen "Hent sager" (objektet "Netforvaltning
  Sundhed (Chrome)"). Returnerer én dict pr. sag med `Blanketnavn`, `Ansvar`, `Afdeling`,
  `Borger`, `Modtager`, `Cpr`, `Oprettelsesdato`, `Besvaret af attestudsteder` og `Status`.
  Datoerne er `date` eller `None`. Ingen sager giver `[]`.

### Brugere (`nfs.brugere`)

- `soeg_bruger(email)` — søg i "Kommunens brugere"
- `naviger_til_bruger(email)` — gå til brugerens detaljeside
- `slet_bruger(email)` — slet brugeren og verificér at den er væk

### Flere browserklienter i samme proces

Playwrights sync-API tillader kun én instans pr. tråd. Skal NFSClient køre sammen med
andre Playwright-baserede klienter (fx oes-client), så start én instans og giv den til
dem alle. Hver klient får stadig sin egen browser, sit eget vindue og sit eget login.
Den delte instans stoppes ikke, når klienten lukkes; det gør `with`-blokken.

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as pw:
    with NFSClient(base_url, username, password, playwright=pw) as nfs, \
         OESClient(anden_url, username, password, playwright=pw) as oes:
        ...
```

Uden `playwright` (standard) starter og stopper klienten sin egen instans som hidtil.

## Arkitektur

- `NFSSession` (`session.py`) ejer browseren og login.
- Hvert område er en lille klient, der får sessionen: `SagerClient` (`sager.py`),
  `BrugerClient` (`brugere.py`).
- `NFSClient` (`client.py`) opretter sessionen og områderne og samler dem som `nfs.sager`,
  `nfs.brugere`.

Nyt område: opret `nfs_client/<omraade>.py` med `class XClient: def __init__(self, session)`,
læg selectors i `selectors.py`, tilføj `self.<omraade> = XClient(self.session)` i `NFSClient`, og
skriv `tests/test_<omraade>.py` med `nfs`-fixturen.

## Ændringer i 0.5.0

- `NFSClient(..., playwright=pw)` tager en valgfri, delt Playwright-instans, så
  flere browserklienter kan køre i samme proces. Uden den opfører klienten sig
  som før. Ingen brud på API'et.

## Ændringer i 0.4.0

Brud på API'et:

- `NFSClient(...).slet_bruger(e)` → `nfs.brugere.slet_bruger(e)` (tilsvarende
  `naviger_til_bruger`)
- `NFSClient(...)._søg_bruger(e)` → `nfs.brugere.soeg_bruger(e)`

## Test

Kopier `.env.example` til `.env` og udfyld. `tests/conftest.py` indlæser `.env` selv. Tests mod
NFS springes over, hvis `BASE_URL`, `NFS_USERNAME` eller `NFS_PASSWORD` mangler.

```bash
uv run pytest tests/test_sager.py -k parse   # offline
uv run pytest                                # alle, mod NFS (logger ind én gang)
```

`tests/test_sager.py` kræver `TEST_NFS_CPR` (og evt. `TEST_NFS_CPR_UDEN_SAGER`),
`tests/test_brugere.py` kræver `TEST_EMAIL`. Tests der ændrer data i NFS (`slet_bruger`) kræver
desuden `NFS_ALLOW_WRITE=1`.

## Afhængigheder

| Pakke | Formål |
|---|---|
| `playwright` | Browserautomatisering af NFS-webgrænsefladen |
| `authlib` | OAuth/autentificering (til fremtidige auth-flows) |
| `httpx` | HTTP-klient (til fremtidige REST API-integrationer) |
| `pytest` | Testframework til integrationstest |
| `ruff` (dev) | Linter og kodeformatter |
| `python-dotenv` (dev) | Indlæser `.env` i testene |

## Licens

MIT
