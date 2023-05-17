import configparser
import os
import importlib

import pytest
import requests


from BAMapi.exceptions import InvalidAPIKeys, RateLimitExceededError
from BAMapi.constants import INSTRUMENTS
from BAMapi.utils import (
    _base_bam_api_get_request,
    _is_valid_date_string,
    _check_currency_label,
    _search_instruments_const,
)


def test_base_bam_api_get_request(mock_requests_get, psudo_args_base_req, sample_data):
    mock_requests_get.json.return_value = sample_data

    response = _base_bam_api_get_request(*psudo_args_base_req)

    assert all(isinstance(item, dict) for item in response)
    assert response == sample_data


@pytest.mark.parametrize(
    "status_code, error", [(401, InvalidAPIKeys), (429, RateLimitExceededError)]
)
def test_base_bam_api_get_request_raises_errors(
    status_code, error, mock_requests_get, psudo_args_base_req
):
    mock_requests_get.status_code = status_code
    with pytest.raises(error):
        _base_bam_api_get_request(*psudo_args_base_req)


@pytest.mark.parametrize(
    "date, date_format",
    [
        ("2023-01-01", ["%Y-%m-%d", "%Y-%m-%dT%H:%M:%S.%fZ"]),
        ("2023-05-13T14:30:00.000000Z", ["%Y-%m-%d", "%Y-%m-%dT%H:%M:%S.%fZ"]),
        ("2024-01-01", "%Y-%m-%d"),
        ("", "%Y-%m-%d"),
    ],
)
def test_is_valid_date_string(date, date_format):
    assert _is_valid_date_string(date, date_format) is True


@pytest.mark.parametrize(
    "date, date_format, strict",
    [
        (10, ["%Y-%m-%d", "%Y-%m-%dT%H:%M:%S.%fZ"], False),
        (object, 10, False),
        ("05-2023-13T14:30:00.000000Z", ["%Y-%m-%d", "%Y-%m-%dT%H:%M:%S.%fZ"], False),
        ("2024-00-00", "%Y-%m-%d", False),
        ("", "%Y-%m-%d", True),
        (" ", "%Y-%m-%d", False),
    ],
)
def test_is_valid_date_string_errors(date, date_format, strict):
    with pytest.raises((ValueError, TypeError)):
        _is_valid_date_string(date, date_format, strict)


def test_check_currency_label(faker):
    faker.seed = 0
    for currency in [faker.currency_code() for _ in range(10)]:
        _check_currency_label(currency)


@pytest.mark.parametrize("currency", [10, 12.25, object, "MADD", "CAAD", "$"])
def test_check_currency_label_errors(currency):
    with pytest.raises(ValueError):
        _check_currency_label(currency)


@pytest.mark.parametrize(
    "name, acronym", [(name, acronym) for name, acronym in INSTRUMENTS.items()]
)
def test_search_instruments_const_by_name(name, acronym):
    assert _search_instruments_const(name) == acronym


@pytest.mark.parametrize("acronym", [acronym for acronym in INSTRUMENTS.values()])
def test_search_instruments_const_by_acronym(acronym):
    assert _search_instruments_const(acronym) == acronym


@pytest.mark.parametrize("search_key", ["", ""])
def test_search_instruments_const_empty_string(search_key):
    assert _search_instruments_const(search_key) == search_key


@pytest.mark.parametrize(
    "search_key", [10, object, "invalid_name", "invalid_acronym", " "]
)
def test_search_instruments_const_error(search_key):
    with pytest.raises(ValueError):
        _search_instruments_const(search_key)
