def test_login(nfs_client):
    nfs_client.login()
    breakpoint = ""


def test_fremsøg_bruger(nfs_client, email=""):
    nfs_client.login()
    nfs_client.fremsøg_bruger(email)
    #Fejler for nu grundet email og søg, men der bliver navigeret over til 'kommunens brugere' korrekt


def test_close(nfs_client):
    nfs_client.login()
    nfs_client.close()