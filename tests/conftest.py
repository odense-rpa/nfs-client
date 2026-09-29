import os
from pathlib import Path

import pytest
from dotenv import load_dotenv

from nfs_client import NFSClient

# testindstillinger læses eksplicit fra .env i projektroden
# // test settings are loaded explicitly from .env in the project root
load_dotenv(Path(__file__).parent.parent / ".env")


def _nfs_login() -> dict:
    """Login-indstillinger til NFS - springer testen over hvis de mangler."""
    manglende = [
        navn
        for navn in ("BASE_URL", "NFS_USERNAME", "NFS_PASSWORD")
        if not os.getenv(navn)
    ]
    if manglende:
        pytest.skip(f"Mangler i .env: {', '.join(manglende)}")
    return {
        "base_url": os.environ["BASE_URL"],
        "username": os.environ["NFS_USERNAME"],
        "password": os.environ["NFS_PASSWORD"],
    }


@pytest.fixture(scope="session")
def nfs():
    """Én indlogget NFSClient for hele testkørslen // One login per test run."""
    client = NFSClient(**_nfs_login(), headless=False)
    yield client
    client.close()


@pytest.fixture
def tillad_skriv():
    """Springer tests over der ændrer data i NFS, medmindre NFS_ALLOW_WRITE=1."""
    if os.getenv("NFS_ALLOW_WRITE") != "1":
        pytest.skip("ændrer data i NFS - sæt NFS_ALLOW_WRITE=1")


def _env_eller_spring_over(navn: str) -> str:
    vaerdi = os.getenv(navn)
    if not vaerdi:
        pytest.skip(f"{navn} er ikke sat")
    return vaerdi


@pytest.fixture
def test_mail():
    return _env_eller_spring_over("TEST_EMAIL")


@pytest.fixture
def test_nfs_cpr():
    return _env_eller_spring_over("TEST_NFS_CPR")


@pytest.fixture
def test_nfs_cpr_uden_sager():
    return _env_eller_spring_over("TEST_NFS_CPR_UDEN_SAGER")
