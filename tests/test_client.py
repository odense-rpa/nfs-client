import pytest

def test_login(nfs_client):
    nfs_client.login()
    breakpoint = ""


def test_fremsøg_bruger(nfs_client):
    nfs_client.login()
    test_email = "marsn@odense.dk"
    nfs_client.fremsøg_bruger(test_email)


def test_close(nfs_client):
    nfs_client.login()
    nfs_client.close()