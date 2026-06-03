import pytest
import os

from nfs_client.client import NFSClient


@pytest.fixture
def nfs_client():
    return NFSClient(
        base_url=os.getenv("BASE_URL"),
        username=os.getenv("USERNAME"),
        password=os.getenv("PASSWORD")
    )
