from unittest.mock import patch
from pathlib import Path
import json

import requests
import pytest

@pytest.fixture(scope = "function")
def mock_requests_get():
    """Requests get method mock object."""
    with patch.object(requests,'get') as MockResponse:
        yield MockResponse.return_value


@pytest.fixture(scope = "session", name = "psudo_args_base_req")
def psudo_args_for_base_bam_api_get_request():
    return "01651320651", "https://invalid_url.BAMAPI", {"pusdo": "psudo"}


@pytest.fixture(scope = "session")
def sample_data():
    path = Path(__file__).with_name("sample_cours_bbe.json")
    path = new_path = path.parent / "samples" / path.name
    with open(path, 'r') as f:
        return json.load(f)