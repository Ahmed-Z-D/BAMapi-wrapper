from types import MappingProxyType

from BAMapi.utils import _load_api_keys


BASE_URL = "https://api.centralbankofmorocco.ma/"

KEYS = _load_api_keys()

INSTRUMENTS = MappingProxyType(
    {
        "avances_7j": "AVANCES7J",
        "avances_24h": "AVANCES24H",
        "opérations_de_réglage_fin_pension_livrée": "PENSLRF",
        "opérations_de_long_terme_pension_livrée": "PENSLLT",
        "opérations_de_long_terme_prêt_garanti": "PRETGAR",
    }
)

API = MappingProxyType(
    {
        # Marché obligataire:
        "courbe_BDT": BASE_URL + "mo/Version1/api/CourbeBDT",
        # Cours de change:
        "cours_BBE": BASE_URL + "cours/Version1/api/CoursBBE",
        "cours_virement": BASE_URL + "cours/Version1/api/CoursVirement",
        # Marché des adjudications des bons du Trésor:
        "oprts_de_PM": BASE_URL + "adju/Version1/api/GenTELADJ",
        "emissions_de_BT": BASE_URL + "adju/Version1/api/TELADJAdjuNormal",
        "oprts_rachat_de_BT": BASE_URL + "adju/Version1/api/TELADJRachat",
        "oprts_echange_de_BT": BASE_URL + "adju/Version1/api/TELADJEchange",
    }
)
