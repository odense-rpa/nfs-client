import pytest

def test_login(nfs_client):
    nfs_client.login()
    breakpoint = ""


def test_fremsøg_bruger(nfs_client):
    nfs_client.login()
    test_email = "marsn@odense.dk"
    result_row = nfs_client.fremsøg_bruger(test_email, click_details=False)
    assert result_row.count() == 1
    assert result_row.locator("td:nth-child(2)").inner_text().strip().lower() == test_email.lower()


def test_close(nfs_client):
    nfs_client.login()
    nfs_client.close()


def test_slet_bruger(nfs_client):
    nfs_client.login()
    nfs_client.fremsøg_bruger()
    nfs_client.slet_bruger()
    # TODO: assert user is deleted
    pass