import pytest
from scope3ai.constants import CLIENTS, try_provider_for_client


@pytest.mark.parametrize(
    "client",
    [client for client in CLIENTS],
)
def test_client_to_provider(client):
    try_provider_for_client(client)
