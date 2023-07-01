#  BAM Api Wrapper

[![LICENSE](https://img.shields.io/github/license/ResidentMario/missingno.svg)](https://github.com/Ahmed-Z-D/BAMapi-wrapper/blob/main/LICENSE) [![Tests](https://github.com/Ahmed-Z-D/BAMapi-wrapper/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/Ahmed-Z-D/BAMapi-wrapper/actions/workflows/tests.yml) [![codecov](https://codecov.io/gh/Ahmed-Z-D/BAMapi-wrapper/branch/main/graph/badge.svg?token=GV7UBRG2ZN)](https://codecov.io/gh/Ahmed-Z-D/BAMapi-wrapper) [![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/) [![CodeFactor](https://www.codefactor.io/repository/github/ahmed-z-d/bamapi-wrapper/badge)](https://www.codefactor.io/repository/github/ahmed-z-d/bamapi-wrapper)


BAMapi is a Python wrapper that streamlines the process of accessing and utilizing Bank Al-Maghrib's API. This API offers a small set of resources provided by the Moroccan central bank for developers to use in their own applications. To obtain additional information about the API, you can refer to its official [documentation](https://apihelpdesk.centralbankofmorocco.ma/docs/services/).

> It is worth noting that in order to avoid any confusion while using this package, the functions have intentionally been named to reflect the names of the endpoints in the API documentation. This naming convention ensures consistency and clarity, making it easier for users to understand and work with the package.

## Installation

Use the following commands to install the package:
```
git clone https://github.com/Ahmed-Z-D/BAMapi-wrapper.git
```
```
cd BAMapi-wrapper
```
```
pip install .
```

## Usage

- [Import the package](#import-the-package)
- [API Keys](#api-keys)
    - [Get the API keys](#get-the-api-keys)
    - [Store the API keys](#store-the-api-keys)
- [Availble Services & Functions](#availble-services-&-functions)
    - [Cours de change](#cours-de-change)
        - [Les cours des billets de Banque étrangers de la journé- Banknote](#les-cours-des-billets-de-banque-étrangers-de-la-journé--banknote)
        - [Les cours virements de la journée - Transfers](#les-cours-virements-de-la-journée---transfers)
    - [Taux de référence des bons du Trésor](#taux-de-référence-des-bons-du-trésor)
        - [Courbe des Taux BDT](#courbe-des-taux-bdt)
    - [Marché des adjudications des bons du Trésor](#marché-des-adjudications-des-bons-du-trésor)
        - [Résultat des opérations de la politique monétaire](#résultat-des-opérations-de-la-politique-monétaire)
        - [Résultats des émissions de bons du Trésor](#résultats-des-émissions-de-bons-du-trésor)
        - [Résultats des opérations d'échange de bons du Trésor](#résultats-des-opérations-d'échange-de-bons-du-trésor)

### Import the package

```python
import BAMapi as bam
```

### API Keys

#### Get the API keys

In order to utilize the services provided by the Bank Al-Maghrib API, developers are required to obtain unique API keys. This can be done with ease by accessing the developer services platform, which is provided by Bank Al-Maghrib at the following link: https://apihelpdesk.centralbankofmorocco.ma/.

#### Store the API keys

Upon obtaining your API key(s), you may utilize the following function to store them:

```python
bam.set_api_keys(
    marche_adjud_des_BT = 'XXXXXXXXXXXXXXXX',
    marche_des_changes = 'XXXXXXXXXXXXXXXX',
    marche_obligataire = 'XXXXXXXXXXXXXXXX'
)
```
To overwrite a specific key, it is sufficient to call the function with the appropriate new key for the given service.

```python
bam.set_api_keys(marche_des_changes = 'XXXXXXXXXXXXXXXXX')
```
You can exhibit the provided API keys by:
```python
bam.display_api_keys()
```
```bash
{'marche_adjud_des_BT': 'XXXXXXXXXXXXXXXX',
'marche_des_changes': 'XXXXXXXXXXXXXXXX',
'marche_obligataire': 'XXXXXXXXXXXXXXXX'}
```

> Should you desire to irrevocably remove the keys, you may achieve this by deleting the "config.ini" file that is situated within the BAMapi directory of the source code.

## Availble Services & Functions

---

### Cours de change

#### Les cours des billets de Banque étrangers de la journé- Banknotes

As per the API's documentation, the exchange rates for foreign banknotes are accessible daily from 8:30 AM (local time). It should be noted that exchange rates are not obtainable on public holidays in Morocco, as well as on the 25th and 26th of December.

```python
bam.cours_BBE()
```
```bash
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
...]
```
Parameters:

- `currency_label` (Optional): retrieves exchange rates for all available currencies if no specific currency label, such as EUR or USD, is provided. The default value for the currency label is an empty string.

- `date_time` (Optional): The date_time parameter denotes the precise date and time when the exchange rates were retrieved and should be presented as a string in accordance with the ISO 8601 date format. The accepted formats include` '%Y-%m-%d `and `'%Y-%m-%dT%H:%M:%S.%fZ`'. If no input is provided for the date_time parameter, the function will default to the current date and `T08:30:00 `as the default time.

#### Les cours virements de la journée - Transfers
According to the API's documentation, exchange rates for transfers made on the current day are accessible from 12:30 PM (local time). It should be noted that there are no exchange rates available on public holidays in Morocco, as well as on the 25th and 26th of December.

```python
bam.cours_virement()
```
```bash
[{'date': '2023-05-11T12:30:00',
  'libDevise': 'EUR',
  'moyen': 10.9884,
  'uniteDevise': 1},
{'date': '2023-05-11T12:30:00',
  'libDevise': 'CAD',
  'moyen': 7.5001,
  'uniteDevise': 1},
...]
```

Parameters:

> The available optional parameters are `currency_label` and `date_time`. It is advised to consult the description of the aforementioned parameters in "Banknotes" for further details.

---

### Taux de référence des bons du Trésor

#### Courbe des Taux BDT

> It should be noted that the volume is expressed in millions of Moroccan Dirhams.

```python
bam.courbe_BDT("2019-01-02")
```
```bash
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
...]
```
Parameters:

- `date` (optional): The date parameter must conform to the ISO 8601 date format, such as '2019-01-02'. In case a specific date is not provided, the function defaults to the previous day's date. The default value for the date parameter is an empty string.

---

### Marché des adjudications des bons du Trésor

#### Résultat des opérations de la politique monétaire

```python
bam.resultat_oprts_politique_monetaire(date_adjudication_du = "2023-01-01")
```

```bash
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
...]
```

Parameters:

* `date_adjudication_du`: Date Adjudication Du Format(AAAA-MM-JJ)

* `date_adjudication_au` (Optional): Date Adjudication Au Format(AAAA-MM-JJ).

* `instrument` (Optional): Filter the results based on the name or acronym of an instrument. The list of available instruments includes:

<div align="center">

| Name                                     | Acronym   |
|------------------------------------------|-----------|
| avances_7j                               | AVANCES7J |
| avances_24h                              | AVANCES24H|
| opérations_de_réglage_fin_pension_livrée | PENSLRF   |
| opérations_de_long_terme_pension_livrée  | PENSLLT   |
| opérations_de_long_terme_prêt_garanti    | PRETGAR   |

</div>

You can obtain this list as a Mapping Proxy by:

```python
bam.INSTRUMENTS
```
```bash
mappingproxy({'avances_7j': 'AVANCES7J',
              'avances_24h': 'AVANCES24H',
              'opérations_de_réglage_fin_pension_livrée': 'PENSLRF',
              'opérations_de_long_terme_pension_livrée': 'PENSLLT',
              'opérations_de_long_terme_prêt_garanti': 'PRETGAR'})

```

#### Résultats des émissions de bons du Trésor

```python
bam.resultats_emissions_BT(date_reglement = "2022-04-04")
```
```bash
[{'dateReglement': '2022-04-04T00:00:00',
  'maturite': '2 ans',
  'caracteristique': '16/09/2024,1.85',
  'mntPropose': 1560.0,
  'tauxPrixMin': 99.62,
  'tauxPrixMax': 99.92,
  'mntAdjuge': 0.0,
  'tauxPrixlimite': 0.0,
  'tauxPrixMoyenPondere': 0.0},
 {'dateReglement': '2022-04-04T00:00:00',
  'maturite': '30 ans',
  'caracteristique': '20/02/2051,3.45',
  'mntPropose': 100.0,
  'tauxPrixMin': 99.89,
  'tauxPrixMax': 99.89,
  'mntAdjuge': 0.0,
  'tauxPrixlimite': 0.0,
  'tauxPrixMoyenPondere': 0.0},
...]
```
Parameters:

* `date_reglement`: Date règlement de la séance d'adjudication Format(AAAA-MM-JJ) ("2022-04-04")

#### Résultats des opérations d'échange de bons du Trésor

```python
bam.resultats_oprts_echange_BT(date_reglement = "2023-04-25")
```
```bash
[{'maturite': '5 ans',
  'dateReglement': '2023-04-25T00:00:00',
  'dateEcheance': '2024-04-15T00:00:00',
  'tauxNominal': 2.85,
  'mntPropose': 855.0,
  'mntRetenu': 855.0,
  'maturiteRemp': '2 ans',
  'dateEcheanceRemp': '2025-09-15T00:00:00',
  'tauxNominallRemp': 3.9,
  'prixMin': 99.74,
  'prixMax': 99.75,
  'mntRetenuRemp': 852.3,
  'pmp': 100.42},
... ]
```

Parameters:

* `date_reglement`: Date règlement de la séance d'adjudication Format(AAAA-MM-JJ) ("2023-04-25")