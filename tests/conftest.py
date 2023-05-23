import json
from unittest.mock import patch
from pathlib import Path
from dataclasses import dataclass

import requests
import pytest

from BAMapi.utils import _initiate_config_file


@dataclass
class PsudoConfFileData:
    """Rand data for config file"""

    marche_adjud_des_BT: str
    marche_des_changes: str
    marche_obligataire: str


@pytest.fixture(scope="function")
def mock_requests_get():
    """Requests get method mock object."""
    with patch.object(requests, "get") as MockResponse:
        yield MockResponse.return_value


@pytest.fixture(scope="session", name="psudo_args_base_req")
def psudo_args_for_base_bam_api_get_request():
    return "01651320651", "https://invalid_url.BAMAPI", {"key": "value"}


@pytest.fixture(scope="session")
def sample_data():
    path = Path(__file__).with_name("sample_cours_bbe.json")
    path = path.parent / "samples" / path.name
    with open(path, "r") as f:
        return json.load(f)


@pytest.fixture(scope="function")
def config_file_path(tmp_path):
    """Provied the path of the cofig file."""
    return tmp_path.parent / "config.ini"


@pytest.fixture(scope="function")
def psudo_conf_file(config_file_path, monkeypatch, faker):
    monkeypatch.setattr("BAMapi.utils._FILE_PATH", config_file_path)

    _initiate_config_file()

    marche_adjud_des_BT = faker.ean13()
    marche_des_changes = faker.ean13()
    marche_obligataire = faker.ean13()

    return PsudoConfFileData(
        marche_adjud_des_BT,
        marche_des_changes,
        marche_obligataire,
    )
