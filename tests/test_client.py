import pytest

def test_søg_bruger(nfs_client, test_mail):
    try:
        nfs_client._søg_bruger(test_mail)
    except Exception as e:
        pytest.fail(f"_søg_bruger raised unexpected exception: {e}")

def test_naviger_til_bruger(nfs_client, test_mail):    
    nfs_client._søg_bruger(test_mail)

    try:
        nfs_client.naviger_til_bruger(test_mail)
    except Exception as e:
        pytest.fail(f"naviger_til_bruger raised unexpected exception: {e}")


def test_close(nfs_client):    
    nfs_client.close()


def test_slet_bruger(nfs_client, test_mail):    
    nfs_client.slet_bruger(test_mail)