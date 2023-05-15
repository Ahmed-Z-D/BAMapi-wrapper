#  BAM Api Wrapper

![Tests](https://github.com/mCodingLLC/SlapThatLikeButton-TestingStarterProject/actions/workflows/tests.yml/badge.svg)

BAMapi is a lightweight and user-friendly Python wrapper that streamlines the process of accessing and utilizing the Bank Al-Maghrib API. This API offers a set of resources provided by the Moroccan central bank for developers to use in their own applications. By using BAMapi, developers can more easily explore and utilize the various APIs that are available from the Moroccan central bank.

BAMapi provides the responses from the endpoint as received without any changes. However, BAMapi validates the inputs sent to the endpoint to maintain data integrity. Each input is checked against the expected format or data type according to the API documentation. This validation process helps prevent the occurrence of errors or inconsistencies which may result from incorrect or invalid data sent to the endpoint.

To avoid any confusion while utilizing this package, the function names have been deliberately maintained as they are named in the API documentation, with minimal to no modifications. This approach ensures consistency and clarity in the function naming convention, making it easier for users to understand and work with the package. Therefore, users may encounter non-English function names while working with the package, but they can rest assured that these names accurately reflect the corresponding functions provided by the API documentation.

## How to Access To the API?

In order to utilize the services provided by the Bank Al-Maghrib API, developers are required to obtain unique API keys. This can be done with ease by accessing the developer services platform, which is provided by Bank Al-Maghrib, at the following URL: https://apihelpdesk.centralbankofmorocco.ma/.

Upon obtaining your API key(s), you may utilize the following function to store them:

```python
import BAMapi as bam

bam.set_api_keys(marche_adjud_des_BT = 'XXXXXXXXXXXXXXXX',
    marche_des_changes = 'XXXXXXXXXXXXXXXX',
    marche_obligataire = 'XXXXXXXXXXXXXXXX')
```
To overwrite a specific key, it is sufficient to call the function with the appropriate new key for the given service.

You can exhibit the provided API keys by:
```python
bam.api_keys()
```
```python
{'marche_adjud_des_BT': 'XXXXXXXXXXXXXXXX',
'marche_des_changes': 'XXXXXXXXXXXXXXXX',
'marche_obligataire': 'XXXXXXXXXXXXXXXX'}

```


# Availble Services / Functions

## Cours de change

### Les cours des billets de Banque étrangers de la journé- Banknotes

As per the API's documentation, the exchange rates for foreign banknotes are accessible daily from 8:30 AM (local time). It should be noted that exchange rates are not obtainable on public holidays in Morocco, as well as on the 25th and 26th of December.

```python
bam.cours_BBE()
```
```python
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
```
Arguments:
- `currency_label` (Optional): retrieves exchange rates for all available currencies if no specific currency label, such as EUR or USD, is provided. The default value for the currency label is an empty string.

- `date_time` (Optional): The date_time parameter denotes the precise date and time when the exchange rates were retrieved and should be presented as a string in accordance with the ISO 8601 date format. The accepted formats include` '%Y-%m-%d `and `'%Y-%m-%dT%H:%M:%S.%fZ`'. If no input is provided for the date_time parameter, the function will default to the current date and `T08:30:00 `as the default time.

### Les cours virements de la journée - Transfers
According to the API's documentation, exchange rates for transfers made on the current day are accessible from 12:30 PM (local time). It should be noted that there are no exchange rates available on public holidays in Morocco, as well as on the 25th and 26th of December.

```python
bam.cours_virement()
```
```python
  [{'date': '2023-05-11T12:30:00',
    'libDevise': 'EUR',
    'moyen': 10.9884,
    'uniteDevise': 1},
   {'date': '2023-05-11T12:30:00',
    'libDevise': 'CAD',
    'moyen': 7.5001,
    'uniteDevise': 1},
    .... ]
```

Arguments:

> Same arguments as Banknotes

## Taux de référence des bons du Trésor

### Courbe des Taux BDT:

It should be noted that the volume is expressed in millions of Moroccan Dirhams.

Arguments:

- date (optional): The date parameter must conform to the ISO 8601 date format, such as '2019-01-02'. In case a specific date is not provided, the function defaults to the previous day's date. The default value for the date parameter is an empty string.

```python
bam.courbe_BDT("2019-01-02")
```
```python
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
  'volume': 155.11},
..]
```

## Marché des adjudications des bons du Trésor

### Résultat des opérations de la politique monétaire

```python
bam.resultat_oprts_politique_monetaire(date_adjudication_du = "2023-01-01")
```

```python
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
```

Arguments:

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

### Résultats des émissions de bons du Trésor

```python
bam.resultats_emissions_BT(date_reglement = "2022-04-04")
```

```python
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
  ... ]
```
Arguments:

        date_reglement:
            Date règlement de la séance d'adjudication Format(AAAA-MM-JJ) exp; "2022-04-04"

### Résultats des opérations d'échange de bons du Trésor

```python
bam.resultats_oprts_echange_BT(date_reglement = "2022-04-04")
```
```python
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
 {'maturite': '5 ans',
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

Arguments:

        date_reglement:
            Date règlement de la séance d'adjudication Format(AAAA-MM-JJ) exp; "2022-04-04"