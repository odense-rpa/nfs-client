"""Tests af sagssøgning // Case search tests.

Parser-testene kører offline med opdigtede data. Tests mod NFS kræver TEST_NFS_CPR og
kontrollerer kun strukturen - de skriver ikke personoplysninger ud.
"""

from datetime import date

import pytest

from nfs_client.sager import KOLONNER, _parse_raekker

HEADER = [
    "Blanketnavn",
    "Ansvar",
    "Afdeling",
    "Borger",
    "Modtager",
    "Cpr",
    "Oprettelsesdato",
    "Besvaret af\nattestudsteder",
    "Status",
    "",
]


def test_parse_raekker():
    raekker = [
        HEADER,
        [
            "LÆ121-LÆ125",
            "Test Testesen\n(tte)",
            "ÆHF, Myndighed",
            "Opdigtet Borger (0101011234)",
            "Lægerne i Testby",
            "0101011234",
            "08-02-2026",
            "20-02-2026",
            "Sagen er afsluttet og arkiveret",
            "Vis sag",
        ],
        [
            "LÆ135",
            "Test Testesen (tte)",
            "ÆHF",
            "Opdigtet Borger (0101011234)",
            "Lægerne i Testby",
            "0101011234",
            "17-02-2026",
            "",
            "Sagen er sendt elektronisk til attestudsteder",
            "Vis sag",
        ],
        # pager-række // pager row
        ["1 2"],
    ]

    sager = _parse_raekker(raekker)

    assert len(sager) == 2
    besvaret, ubesvaret = sager
    assert set(besvaret) == set(KOLONNER)
    assert besvaret["Blanketnavn"] == "LÆ121-LÆ125"
    assert besvaret["Ansvar"] == "Test Testesen (tte)"
    assert besvaret["Cpr"] == "0101011234"
    assert besvaret["Oprettelsesdato"] == date(2026, 2, 8)
    assert besvaret["Besvaret af attestudsteder"] == date(2026, 2, 20)
    assert ubesvaret["Besvaret af attestudsteder"] is None
    assert ubesvaret["Status"] == "Sagen er sendt elektronisk til attestudsteder"


def test_parse_raekker_tom():
    assert _parse_raekker([]) == []
    assert _parse_raekker([HEADER]) == []


def test_hent_sager_ugyldigt_cpr(nfs):
    with pytest.raises(ValueError):
        nfs.sager.hent_sager("12345")


def test_hent_sager(nfs, test_nfs_cpr):
    sager = nfs.sager.hent_sager(test_nfs_cpr)

    assert len(sager) > 0
    cpr = test_nfs_cpr.replace("-", "")
    for sag in sager:
        assert set(sag) == set(KOLONNER)
        assert sag["Cpr"] == cpr
        assert sag["Oprettelsesdato"] is None or isinstance(
            sag["Oprettelsesdato"], date
        )
        assert sag["Besvaret af attestudsteder"] is None or isinstance(
            sag["Besvaret af attestudsteder"], date
        )


def test_hent_sager_ingen(nfs, test_nfs_cpr_uden_sager):
    assert nfs.sager.hent_sager(test_nfs_cpr_uden_sager) == []


def test_hent_sager_to_gange(nfs, test_nfs_cpr, test_nfs_cpr_uden_sager):
    """Søgesiden nulstilles mellem kald // the search page resets between calls."""
    assert len(nfs.sager.hent_sager(test_nfs_cpr)) > 0
    assert nfs.sager.hent_sager(test_nfs_cpr_uden_sager) == []
