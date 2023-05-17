import configparser
import os
import importlib

import pytest
from faker import Faker

from BAMapi.utils import _initiate_config_file, _load_api_keys
from BAMapi.api import (
    set_api_keys,
    display_api_keys,
    _base_foreign_exchange_rates,
    cours_BBE,
    cours_virement,
    courbe_BDT,
    resultat_oprts_politique_monetaire,
    resultats_emissions_BT,
    resultats_oprts_echange_BT,
)


def test_initiate_config_file(config_file_path, monkeypatch):
    # monkeypatch _FILE_PATH const; new value: config_file_path instead of __file__
    target = importlib.import_module("BAMapi.utils")
    monkeypatch.setattr(target, "_FILE_PATH", config_file_path)

    _initiate_config_file()

    # check if the file has been configurated correctly
    config = configparser.ConfigParser()
    config.read(config_file_path)

    assert config["APIkeys"]["marche_adjud_des_BT"] == ""
    assert config["APIkeys"]["marche_des_changes"] == ""
    assert config["APIkeys"]["marche_obligataire"] == ""


def test_load_api_keys(config_file_path, monkeypatch):
    target = importlib.import_module("BAMapi.utils")
    monkeypatch.setattr(target, "_FILE_PATH", config_file_path)

    api_keys = _load_api_keys()

    valid_keys = ["marche_adjud_des_BT", "marche_des_changes", "marche_obligataire"]

    assert set(valid_keys) == set([k for k in api_keys.keys()])
    assert set(["", "", ""]) == set([v for v in api_keys.values()])


def test_display_api_keys(config_file_path, capsys, monkeypatch, psudo_conf_file):
    target_path_utils = importlib.import_module("BAMapi.utils")
    monkeypatch.setattr(target_path_utils, "_FILE_PATH", config_file_path)

    target_path_api = importlib.import_module("BAMapi.api")
    monkeypatch.setattr(target_path_api, "_FILE_PATH", config_file_path)

    r = set_api_keys(
        psudo_conf_file.marche_adjud_des_BT,
        psudo_conf_file.marche_des_changes,
        psudo_conf_file.marche_obligataire,
    )

    target_file_consts = importlib.import_module("BAMapi.constants")
    monkeypatch.setattr(target_file_consts, "KEYS", _load_api_keys())
    from BAMapi.constants import KEYS

    display_api_keys()
    output = capsys.readouterr().out.rstrip()

    assert output == str(KEYS)


def test_set_api_keys_first_time(config_file_path, psudo_conf_file, monkeypatch):
    target_path_utils = importlib.import_module("BAMapi.utils")
    monkeypatch.setattr(target_path_utils, "_FILE_PATH", config_file_path)

    target_path_api = importlib.import_module("BAMapi.api")
    monkeypatch.setattr(target_path_api, "_FILE_PATH", config_file_path)

    _initiate_config_file()

    r = set_api_keys(
        psudo_conf_file.marche_adjud_des_BT,
        psudo_conf_file.marche_des_changes,
        psudo_conf_file.marche_obligataire,
    )

    target_file_consts = importlib.import_module("BAMapi.constants")
    monkeypatch.setattr(target_file_consts, "KEYS", _load_api_keys())
    from BAMapi.constants import KEYS

    assert r is True
    assert KEYS["marche_adjud_des_BT"] == psudo_conf_file.marche_adjud_des_BT
    assert KEYS["marche_des_changes"] == psudo_conf_file.marche_des_changes
    assert KEYS["marche_obligataire"] == psudo_conf_file.marche_obligataire


def test_base_foreign_exchange_rates(faker, mock_requests_get, sample_data):
    url = faker.url()
    service_api_key = faker.ean13()
    currency_label = faker.currency_code()
    date_time = faker.date()

    mock_requests_get.json.return_value = sample_data

    response = _base_foreign_exchange_rates(url, currency_label, date_time)

    assert all(isinstance(d, dict) for d in response)
    assert response == sample_data


@pytest.mark.parametrize(
    "currency_label, date_time", [("", ""), (Faker().currency_code(), Faker().date())]
)
def test_cours_BBE(currency_label, date_time, mock_requests_get, sample_data):
    mock_requests_get.json.return_value = sample_data

    response = cours_BBE(currency_label, date_time)

    assert all(isinstance(d, dict) for d in response)
    assert response == sample_data


@pytest.mark.parametrize(
    "currency_label, date_time", [("", ""), (Faker().currency_code(), Faker().date())]
)
def test_cours_virement(currency_label, date_time, mock_requests_get, sample_data):
    mock_requests_get.json.return_value = sample_data

    response = cours_virement(currency_label, date_time)

    assert all(isinstance(d, dict) for d in response)
    assert response == sample_data


@pytest.mark.parametrize("date", ["", Faker().date()])
def test_courbe_BDT(date, mock_requests_get, sample_data):
    mock_requests_get.json.return_value = sample_data

    response = courbe_BDT(date)

    assert all(isinstance(d, dict) for d in response)
    assert response == sample_data


def test_resultat_oprts_politique_monetaire(faker, mock_requests_get, sample_data):
    date_adjudication_du = faker.date()
    date_adjudication_au = ""
    instrument = "avances_7j"

    mock_requests_get.json.return_value = sample_data

    response = resultat_oprts_politique_monetaire(
        date_adjudication_du, date_adjudication_au, instrument
    )

    assert all(isinstance(d, dict) for d in response)
    assert response == sample_data


def test_resultats_emissions_BT(faker, mock_requests_get, sample_data):
    date = faker.date()

    mock_requests_get.json.return_value = sample_data

    response = resultats_emissions_BT(date)

    assert all(isinstance(d, dict) for d in response)
    assert response == sample_data


def test_resultats_oprts_echange_BT(faker, mock_requests_get, sample_data):
    date = faker.date()

    mock_requests_get.json.return_value = sample_data

    response = resultats_oprts_echange_BT(date)

    assert all(isinstance(d, dict) for d in response)
    assert response == sample_data
