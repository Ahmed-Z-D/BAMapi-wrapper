import requests
from datetime import datetime
import re
from typing import Any, List, Dict, Union
import configparser
from pathlib import Path
from types import MappingProxyType

from BAMapi.exceptions import InvalidAPIKeys, RateLimitExceededError


CURRENCY_PATTERN = re.compile(r"^[A-Z]{3}$")


def _base_bam_api_get_request(
    sub_key: str, url: str, querystring: dict
) -> List[Dict]:
    """Base intercation function with BAM's API.

    Args:
        - sub_key:
             The subscription key for the given service.

        - url:
             The endpoint of the service.

        - querystring:
             The query string of the URL.

    Returns:
        The query output could be either a list of dictionaries or an empty list.

    Raises:
        InvalidAPIKey: Invalid API key.
        RateLimitExceededError: Rate limit is exceeded.
        requests.exceptions.RequestException: Request Exceptions.

    """

    headers = {
        "Ocp-Apim-Subscription-Key": f"{sub_key}",
    }

    try:
        response = requests.get(
            url=url, headers=headers, params=querystring, timeout=10
        )

        if response.status_code == 401:
            raise InvalidAPIKeys(
                f"Access has been denied. Kindly verify the authenticity of the API keys that have been provided."
            )
        elif response.status_code == 429:
            raise RateLimitExceededError(response.json()["message"])

        response.raise_for_status()

    except Exception as e:
        raise e

    return response.json()

def _is_valid_date_string(date_string: str, date_formats: Union[str, list[str]], strict: bool=False) -> bool:
    """Validate date string format."""

    if date_string == "" and not strict:
        return True

    if isinstance(date_formats, str):
        try:
            datetime.strptime(date_string, date_formats)
            return True
        except ValueError as e:
            raise e

    for date_format in date_formats:
        try:
            datetime.strptime(date_string, date_format)
            return True
        except ValueError:
            pass

    raise ValueError(
        f"The provided date string is not in a valid format. Please use one of the following valid date format(s): {date_formats}."
        )


def _check_currency_label(currency_label: str) -> bool:
    """Verify whether the provided string adheres to the pattern of a currency label."""
    if not isinstance(currency_label, str):
        raise ValueError(f"Currency label must be of type string.")

    if currency_label:
        if CURRENCY_PATTERN.match(currency_label):
            return True
        else:
            raise ValueError(f"{currency_label} is not a valid currency label.")

def _search_instruments_const(instrument: str) -> str:

    # In order to prevent ImportError due to  circular import, we use this import statment here.
    # TODO: Refactore the code to prevent circular import.
    from BAMapi.constants import INSTRUMENTS

    if instrument == "":
        return instrument

    if isinstance(instrument, str):
        for name, acronym in INSTRUMENTS.items():
            if (instrument.upper() == name.upper()) or (
                instrument.upper() == acronym
            ):
                return acronym

        raise ValueError(
            f"Invalid instrument name or acronym. Please verify the list of availble instruments"
        )

    raise ValueError(
        f"Invalid instrument dtype. Please verify the list of availble instruments"
    )

def _initiate_config_file(config_file_path: Path) -> None:
    """Initiate the default config.ini file.

    Args:
        config_file_path; Path to the config.ini file.

    Returns:
        None
    """
    if not config_file_path.exists():
        config = configparser.ConfigParser()

        config["APIkeys"] = {
            "marche_adjud_des_BT": "",
            "marche_des_changes": "",
            "marche_obligataire": "",
        }

        with open(config_file_path, "w") as f:
            config.write(f)

def _load_api_keys(_test_path=False) -> dict:
    """ Lead Api Keys to KEYS const."""
    if not _test_path:
        config_file_path = Path(__file__).with_name("config.ini")
    else:
        config_file_path = _test_path


    _initiate_config_file(config_file_path)
    config = configparser.ConfigParser()
    config.read(config_file_path)

    keys = dict()
    keys["marche_adjud_des_BT"] = config["APIkeys"]["marche_adjud_des_BT"]
    keys["marche_des_changes"] = config["APIkeys"]["marche_des_changes"]
    keys["marche_obligataire"] = config["APIkeys"]["marche_obligataire"]

    return keys