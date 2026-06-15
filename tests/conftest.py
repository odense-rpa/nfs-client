import pytest
import os

from nfs_client.client import NFSClient


@pytest.fixture
def nfs_client():
    return NFSClient(
        base_url=os.getenv("BASE_URL", "about:blank"),
        username=os.getenv("USERNAME", ""),
        password=os.getenv("PASSWORD", ""),
    )


@pytest.fixture
def test_mail():
    return os.getenv("TEST_EMAIL")
