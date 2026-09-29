"""Playwright-klient til Netforvaltning Sundhed (NFS).

Brug:
    from nfs_client import NFSClient

    with NFSClient(base_url, username, password) as nfs:
        sager = nfs.sager.hent_sager(cpr)
"""

from nfs_client.brugere import BrugerClient
from nfs_client.client import NFSClient
from nfs_client.exceptions import NFSFejl
from nfs_client.sager import SagerClient
from nfs_client.session import NFSSession

__all__ = ["BrugerClient", "NFSClient", "NFSFejl", "NFSSession", "SagerClient"]
