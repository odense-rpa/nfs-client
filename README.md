# nfs-client

Playwright-baseret Python-klient til automatisering af brugeradministration i NFS (Nemlig Fælles System) via browserautomatisering.

> Denne klient er ikke officielt støttet eller godkendt af leverandøren bag NFS. Brug på eget ansvar.

## Nuværende funktionalitet

- Autentificering mod NFS-webapplikationen via HTTP basic auth og headless Chromium
- Søgning efter kommunale brugere på e-mailadresse via "Kommunens brugere"
- Navigation til en specifik brugers detaljeside (administratorroller filtreres fra)
- Sletning af en bruger med efterfølgende verifikation af at brugeren ikke længere optræder i søgeresultaterne

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
from nfs_client.client import NFSClient

with NFSClient(
    base_url="https://nfs.example.dk",
    username="brugernavn",
    password="adgangskode",
) as client:
    client.slet_bruger("borger@kommune.dk")
```

Det er også muligt at navigere til en brugers detaljeside uden at slette:

```python
client.naviger_til_bruger("borger@kommune.dk")
```

## Afhængigheder

| Pakke | Formål |
|---|---|
| `playwright` | Browserautomatisering af NFS-webgrænsefladen |
| `authlib` | OAuth/autentificering (til fremtidige auth-flows) |
| `httpx` | HTTP-klient (til fremtidige REST API-integrationer) |
| `pytest` | Testframework til integrationstest |
| `ruff` | Linter og kodeformatter |

## Licens

MIT
