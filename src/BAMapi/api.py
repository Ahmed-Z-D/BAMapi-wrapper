import configparser
from datetime import datetime
from typing import Union, Dict, Any, List
from pathlib import Path

import pandas as pd

from BAMapi.constants import INSTRUMENTS, API, KEYS
from BAMapi.utils import (
    _base_bam_api_get_request,
    _check_currency_label,
    _search_instruments_const,
    _is_valid_date_string,
    _load_api_keys,
    _initiate_config_file,
)


RETRUNED_T = List[Dict[str, Union[str, int, float]]]


def set_api_keys(
    marche_adjud_des_BT: str = "",
    marche_des_changes: str = "",
    marche_obligataire: str = "",
) -> bool:
    """ Set API key(s).

    This function is designed to store primary API keys for each provided service.
    It is important to note that each service has its own unique set of API keys, with two types of
    keys available for each service: primary keys and secondary keys.

    To overwrite a specific key, it is sufficient to call the function with the appropriate new key for
    the given service(s).

    Args:
        marche_adjud_des_BT:
          The primary API key associated with the "Marché des adjudications des bons du Trésor" service.

        marche_des_changes:
          The primary API key associated with the "Marché des changes" service.

        marche_obligataire:
          The primary API key associated with the "Marché obligataire" service.

    Returns:
        bool: If the key(s) have been successfully preserved, the function will return a Boolean value of True.
    """

    global KEYS

    config_file_path = Path(__file__).with_name("config.ini")
    config = configparser.ConfigParser()
    config.read(config_file_path)

    if marche_adjud_des_BT:
        config["APIkeys"]["marche_adjud_des_BT"] = marche_adjud_des_BT
    if marche_des_changes:
        config["APIkeys"]["marche_des_changes"] = marche_des_changes
    if marche_obligataire:
        config["APIkeys"]["marche_obligataire"] = marche_obligataire

    with open(config_file_path, "w") as f:
        config.write(f)

    KEYS = _load_api_keys()

    return True

def api_keys() -> None:
    """Exhibit the API keys provided by the user."""
    print(KEYS)

#===============================
#    Marché des changes
#===============================

def _base_foreign_exchange_rates(
    url: str,
    currency_label: str = "",
    date_time: str = ""
) -> RETRUNED_T:
    """Base Get Request to retrive data from the forieng exchange markt API.

    Args:
        url:
          The targeted service endpoint (Product: Marché des changes)

        currency_label:
          The label of the currency, such as EUR or USD.  If no specific currency
          label is provided, the function will retrieve  exchange rates for all available currencies.
          The default value is "".

        date_time:
          The date_time parameter represents the date and time when the exchange rates
          were retrieved. This argument should be provided as astring in compliance with the
          ISO 8601 date format, using either the '%Y-%m-%d' or the '%Y-%m-%dT%H:%M:%S.%fZ' format.
          If no value is provided for the date_time parameter, it will default to the current date
          and a default time of T08:30:00.

    Returns:
        Refer to RETRUNED_T.

    Raise:
        ValueError: Invalid input(s).
        InvalidAPIKeys: Invalid API key(s).
        RateLimitExceededError: Rate limit on GET requests has exceeded.
        Possibly any exception that has requests.exceptions.RequestException as a base.
    """
    _is_valid_date_string(date_time, ["%Y-%m-%d", "%Y-%m-%dT%H:%M:%S.%fZ'"])
    _check_currency_label(currency_label)

    querystring = {
        "libDevise": currency_label,
        "date": date_time,
    }

    return _base_bam_api_get_request(
        KEYS["marche_des_changes"], url, querystring
    )


def cours_BBE(
    currency_label: str = "",
    date_time: str = ""
) -> RETRUNED_T:
    """Les cours des billets de Banque étrangers de la journée.

    The exchange rates for foreign banknotes are made available for each day starting
    from 8:30 AM (local time). It is important to note that exchange rates are not available
    on public holidays in Morocco, and also on December 25th and 26th.

    Args:
        currency_label:
          The label of the currency, such as EUR or USD.  If no specific currency
          label is provided, the function will retrieve  exchange rates for all available currencies.
          The default value is "".

        date_time:
          The date_time parameter represents the date and time when the exchange rates
          were retrieved. This argument should be provided as astring in compliance with the
          ISO 8601 date format, using either the '%Y-%m-%d' or the '%Y-%m-%dT%H:%M:%S.%fZ' format.
          If no value is provided for the date_time parameter, it will default to the current date
          and a default time of T08:30:00.

    Returns:
        A List of dictionaries that contains the raw JSON response, where each key in a dict is a string type,
        and each dict value can be a string, integer, or floating-point number. For example:

        [{'achatClientele': 2.5085,
          'date': '2023-05-11T08:30:00',
          'libDevise': 'QAR',
          'uniteDevise': 1,
          'venteClientele': 2.9153},
         {'achatClientele': 86.54,
          'date': '2023-05-11T08:30:00',
          'libDevise': 'NOK',
          'uniteDevise': 100,
          'venteClientele': 100.57},
          ... ]

        Please note that if the function receives a GET response with a status code of 204 No Content,
        it will return an empty list.


    Raise:
        ValueError: Invalid input(s).
        InvalidAPIKeys: Invalid API key(s).
        RateLimitExceededError: Rate limit on GET requests has exceeded.
        Possibly any exception that has requests.exceptions.RequestException as a base.
    """

    return _base_foreign_exchange_rates(
        API["cours_BBE"],
        currency_label,
        date_time
    )


def cours_virement(
    currency_label: str = "", date_time: str = ""):
    """Get the exchange rates for bank transfers of the current day or of a given day.

    The current exchange rates for bank transfers (Les cours virements de la journée)
    are made available from 12:30 PM (local time). Please note that there are no quotes for holidays
    in Morocco as well as for the days of 25/12 and 26/12.

    Args:
        currency_label:
          The label of the currency, such as EUR or USD.  If no specific currency
          label is provided, the function will retrieve  exchange rates for all available currencies.
          The default value is "" (empty string).

        date_time:
          The date_time parameter represents the date and time when the exchange rates
          were retrieved. This argument should be provided as astring in compliance with the
          ISO 8601 date format, using either the '%Y-%m-%d' or the '%Y-%m-%dT%H:%M:%S.%fZ' format.
          If no value is provided for the date_time parameter, it will default to the current date
          and a default time of T08:30:00.

    Returns:
        A dictionary that contains the raw JSON response, where each key is a string type, and each value
        can be a string, integer, or floating-point number. For example:

        [{'date': '2023-05-11T12:30:00',
          'libDevise': 'EUR',
          'moyen': 10.9884,
          'uniteDevise': 1},
         {'date': '2023-05-11T12:30:00',
          'libDevise': 'CAD',
          'moyen': 7.5001,
          'uniteDevise': 1},
          .... ]


        Please note that if the function receives a GET response with a status code of 204 (No Content),
        it will return an empty list.

    Raise:
        ValueError: Invalid input(s).
        InvalidAPIKeys: Invalid API key(s).
        RateLimitExceededError: Rate limit on GET requests has exceeded.
        Possibly any exception that has requests.exceptions.RequestException as a base.
    """

    return _base_foreign_exchange_rates(
        API["cours_virement"],
        currency_label,
        date_time
    )


# Marché obligataire:

def courbe_BDT(date: str = "") -> RETRUNED_T:
    """COURBE DES TAUX DE REFERENCE DES BONS DU TRESOR (BDT).

    Get Courbe des Taux BDT. The volume is denoted in units of millions of Moroccan Dirhams.

    Args:
        date:
          The date parameter must adhere to the ISO 8601 date format, for example: '2019-01-02'.
          If a specific date is not provided or specified, the system defaults to the current date
          minus one day. The default value is "" (empty string).

    Returns:
       A list that contains multiple dictionaries. For instance:

            [{'dateEcheance': '2046-02-19',
              'dateValeur': '2018-12-28',
              'dateCourbe': '2019-01-02',
              'tmp': 4.326,
              'volume': 195.25},
             {'dateEcheance': '2036-12-04',
              'dateValeur': '2018-12-31',
              'dateCourbe': '2019-01-02',
              'tmp': 3.762,
              'volume': 32.95},
             {'dateEcheance': '2033-07-18',
              'dateValeur': '2018-12-27',
              'dateCourbe': '2019-01-02',
              'tmp': 3.704,
              'volume': 155.11}]


        Please note that if the function receives a GET response with a status code of 204 (No Content),
        it will return an empty list.

    Raise:
        ValueError: Invalid input(s).
        InvalidAPIKeys: Invalid API key(s).
        RateLimitExceededError: Rate limit on GET requests has exceeded.
        Possibly any exception that has requests.exceptions.RequestException as a base.
    """
    _is_valid_date_string(date, "%Y-%m-%d")

    querystring = {
        "dateCourbe": date,
    }

    return _base_bam_api_get_request(
        KEYS["marche_obligataire"], API["courbe_BDT"], querystring
    )

# Marché des adjudications des bons du Trésor:


def resultat_oprts_politique_monetaire(
    date_adjudication_du: str,
    date_adjudication_au: str = "",
    instrument: str = ""
) -> RETRUNED_T:
    """Résultat des opérations de la politique monétaire.

    Args:
        date_adjudication_du:
            Date Adjudication Du Format(AAAA-MM-JJ)

        date_adjudication_au :optional:
            Date Adjudication Au Format(AAAA-MM-JJ).

        instrument :optional:
          Filter the results based on the name or acronym of an instrument.
          The list of available instruments includes:
                name                                   acronym
            ---------------------------------------------------------
           - avances_7j :                               AVANCES7J
           - avances_24h :                              AVANCES24H
           - opérations_de_réglage_fin_pension_livrée : PENSLRF
           - opérations_de_long_terme_pension_livrée :  PENSLLT
           - opérations_de_long_terme_prêt_garanti :    PRETGAR

          You can obtain this list as a dict by runnig: function name.

    Returns:
        A list that contains multiple dictionaries. For instance:

            [{'dateAdjudication': '2023-01-04',
              'dateValeur': '2023-01-05',
              'dateEcheance': '2023-01-12',
              'instrument': 'avances à 7 jours',
              'mntDemande': 56990.0,
              'mntServi': 56990.0,
              'taux': 2.5},
             {'dateAdjudication': '2023-01-12',
              'dateValeur': '2023-01-12',
              'dateEcheance': '2023-01-19',
              'instrument': 'avances à 7 jours',
              'mntDemande': 48160.0,
              'mntServi': 48160.0,
              'taux': 2.5},
             {'dateAdjudication': '2023-01-23',
              'dateValeur': '2023-01-26',
              'dateEcheance': '2024-01-25',
              'instrument': 'prêt garanti',
              'mntDemande': 95.0,
              'mntServi': 95.0,
              'taux': 1.25},
              ... ]

        Please note that if the function receives a GET response with a status code of 204 (No Content),
        it will return an empty list.

    Raise:
        ValueError: Invalid input(s).
        InvalidAPIKeys: Invalid API key(s).
        RateLimitExceededError: Rate limit on GET requests has exceeded.
        Possibly any exception that has requests.exceptions.RequestException as a base.
    """
    _is_valid_date_string(date_adjudication_du, "%Y-%m-%d")
    _is_valid_date_string(date_adjudication_au, "%Y-%m-%d")

    instrument = _search_instruments_const(instrument)

    querystring = {
        "dateAdjudicationDu": date_adjudication_du,
        "dateAdjudicationAu": date_adjudication_au,
        "instrument": instrument,
    }

    return _base_bam_api_get_request(
        KEYS["marche_adjud_des_BT"], API["oprts_de_PM"], querystring
    )


def resultats_emissions_BT(date_reglement: str):
    """Résultats des émissions de bons du Trésor.

    Args:
        date_reglement:
            Date règlement de la séance d'adjudication Format(AAAA-MM-JJ) exp; "2022-04-04"

    Returns:

    Raise:
        ValueError: Invalid input(s).
        InvalidAPIKeys: Invalid API key(s).
        RateLimitExceededError: Rate limit on GET requests has exceeded.
        Possibly any exception that has requests.exceptions.RequestException as a base.
    """

    _is_valid_date_string(date_reglement, "%Y-%m-%d", True)


    querystring = {"dateReglement": date_reglement}

    return _base_bam_api_get_request(
        KEYS["marche_adjud_des_BT"], API["emissions_de_BT"], querystring
    )


def resultats_oprts_echange_BT(date_reglement: str) -> RETRUNED_T:
    """Résultats des opérations d'échange de bons du Trésor.

    Args:
        date_reglement:
            Date règlement de la séance d'adjudication Format(AAAA-MM-JJ)

    Returns:

    Raise:
        ValueError: Invalid input(s).
        InvalidAPIKeys: Invalid API key(s).
        RateLimitExceededError: Rate limit on GET requests has exceeded.
        Possibly any exception that has requests.exceptions.RequestException as a base.

    """
    _is_valid_date_string(date_reglement, "%Y-%m-%d")

    querystring = {
        "dateReglement": date_reglement,
    }
    return _base_bam_api_get_request(
        KEYS["marche_adjud_des_BT"], API["oprts_echange_de_BT"], querystring
    )