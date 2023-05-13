import configparser
import os

from itertools import combinations

import pytest
from faker import Faker

from BAMapi.constants import KEYS
from BAMapi.api import (
    set_api_keys,
    _base_foreign_exchange_rates,
    cours_BBE,
    cours_virement,
    courbe_BDT,
    resultat_oprts_politique_monetaire,
    resultats_emissions_BT,
    resultats_oprts_echange_BT,
)

@pytest.mark.xfail(reason = "Set API keys does not work as intended")
def test_set_api_keys_first_time(tmp_path, faker):

    __file__ = os.path.join(tmp_path, "config.inin")
    config_file_path = tmp_path.parent / "config.ini"

    marche_adjud_des_BT = faker.ean13()
    marche_des_changes = faker.ean13()
    marche_obligataire = faker.ean13()

    r = set_api_keys(marche_adjud_des_BT, marche_des_changes, marche_obligataire)

    assert r is True
    assert KEYS["marche_adjud_des_BT"] == marche_adjud_des_BT
    assert KEYS["marche_des_changes"] == marche_des_changes
    assert KEYS["marche_obligataire"] == marche_obligataire




def test_base_foreign_exchange_rates(faker, mock_requests_get, sample_data):
    url = faker.url()
    service_api_key = faker.ean13()
    currency_label = faker.currency_code()
    date_time = faker.date()


    mock_requests_get.json.return_value = sample_data

    response = _base_foreign_exchange_rates(url, currency_label, date_time)

    assert all(isinstance(d, dict) for d in response)
    assert response == sample_data


@pytest.mark.parametrize("currency_label, date_time",
    [("", ""),
    (Faker().currency_code(), Faker().date())])
def test_cours_BBE(currency_label, date_time, mock_requests_get, sample_data):

    mock_requests_get.json.return_value = sample_data

    response = cours_BBE(currency_label, date_time)

    assert all(isinstance(d, dict) for d in response)
    assert response == sample_data


@pytest.mark.parametrize("currency_label, date_time",
    [("", ""),
    (Faker().currency_code(), Faker().date())])
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

    response = resultat_oprts_politique_monetaire(date_adjudication_du, date_adjudication_au, instrument)

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