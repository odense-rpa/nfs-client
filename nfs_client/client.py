"""Samlet indgang til NFS // Single entry point to NFS."""

from nfs_client.brugere import BrugerClient
from nfs_client.sager import SagerClient
from nfs_client.session import NFSSession


class NFSClient:
    """Logger ind i NFS og giver adgang til områderne.

    Eksempel:
        with NFSClient(base_url, username, password) as nfs:
            sager = nfs.sager.hent_sager("0101011234")
            nfs.brugere.slet_bruger("bruger@kommune.dk")
    """

    def __init__(
        self,
        base_url: str,
        username: str,
        password: str,
        email: str = "",
        headless: bool | None = None,
    ):
        self.session = NFSSession(base_url, username, password, headless)
        self.brugere = BrugerClient(self.session, email)
        self.sager = SagerClient(self.session)

    def close(self) -> None:
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
