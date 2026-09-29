"""Tests af brugeradministration mod NFS // User admin tests against NFS.

slet_bruger sletter brugeren og kører kun med NFS_ALLOW_WRITE=1.
"""

import pytest

skriv = pytest.mark.usefixtures("tillad_skriv")


def test_soeg_bruger(nfs, test_mail):
    nfs.brugere.soeg_bruger(test_mail)


def test_naviger_til_bruger(nfs, test_mail):
    nfs.brugere.naviger_til_bruger(test_mail)


@skriv
def test_slet_bruger(nfs, test_mail):
    nfs.brugere.slet_bruger(test_mail)
