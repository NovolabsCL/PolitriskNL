# data/all_countries.py
# Catálogo completo de países del mundo con ISO codes y monedas.
# Cubre ~195 países para el mapa interactivo.
# ─────────────────────────────────────────────────────────────────

ALL_COUNTRIES = {
    # ── AMÉRICA LATINA Y EL CARIBE ────────────────────────────────
    "Argentina":          {"iso2":"AR","iso3":"ARG","region":"latin_america","currency":"ARS","fx_pair":"ARSUSD=X"},
    "Bolivia":            {"iso2":"BO","iso3":"BOL","region":"latin_america","currency":"BOB","fx_pair":"BOBUSD=X"},
    "Brasil":             {"iso2":"BR","iso3":"BRA","region":"latin_america","currency":"BRL","fx_pair":"BRLUSD=X"},
    "Chile":              {"iso2":"CL","iso3":"CHL","region":"latin_america","currency":"CLP","fx_pair":"CLPUSD=X"},
    "Colombia":           {"iso2":"CO","iso3":"COL","region":"latin_america","currency":"COP","fx_pair":"COPUSD=X"},
    "Costa Rica":         {"iso2":"CR","iso3":"CRI","region":"latin_america","currency":"CRC","fx_pair":"CRCUSD=X"},
    "Cuba":               {"iso2":"CU","iso3":"CUB","region":"latin_america","currency":"CUP","fx_pair":None},
    "Ecuador":            {"iso2":"EC","iso3":"ECU","region":"latin_america","currency":"USD","fx_pair":None},
    "El Salvador":        {"iso2":"SV","iso3":"SLV","region":"latin_america","currency":"USD","fx_pair":None},
    "Guatemala":          {"iso2":"GT","iso3":"GTM","region":"latin_america","currency":"GTQ","fx_pair":"GTQUSD=X"},
    "Honduras":           {"iso2":"HN","iso3":"HND","region":"latin_america","currency":"HNL","fx_pair":"HNLUSD=X"},
    "Jamaica":            {"iso2":"JM","iso3":"JAM","region":"latin_america","currency":"JMD","fx_pair":"JMDUSD=X"},
    "Mexico":             {"iso2":"MX","iso3":"MEX","region":"latin_america","currency":"MXN","fx_pair":"MXNUSD=X"},
    "Nicaragua":          {"iso2":"NI","iso3":"NIC","region":"latin_america","currency":"NIO","fx_pair":"NIOUSD=X"},
    "Panama":             {"iso2":"PA","iso3":"PAN","region":"latin_america","currency":"USD","fx_pair":None},
    "Paraguay":           {"iso2":"PY","iso3":"PRY","region":"latin_america","currency":"PYG","fx_pair":"PYGUSD=X"},
    "Peru":               {"iso2":"PE","iso3":"PER","region":"latin_america","currency":"PEN","fx_pair":"PENUSD=X"},
    "Rep. Dominicana":    {"iso2":"DO","iso3":"DOM","region":"latin_america","currency":"DOP","fx_pair":"DOPUSD=X"},
    "Trinidad y Tobago":  {"iso2":"TT","iso3":"TTO","region":"latin_america","currency":"TTD","fx_pair":"TTDUSD=X"},
    "Uruguay":            {"iso2":"UY","iso3":"URY","region":"latin_america","currency":"UYU","fx_pair":"UYUUSD=X"},
    "Venezuela":          {"iso2":"VE","iso3":"VEN","region":"latin_america","currency":"VES","fx_pair":None},

    # ── NORTEAMÉRICA ──────────────────────────────────────────────
    "Canada":             {"iso2":"CA","iso3":"CAN","region":"north_america","currency":"CAD","fx_pair":"CADUSD=X"},
    "Estados Unidos":     {"iso2":"US","iso3":"USA","region":"north_america","currency":"USD","fx_pair":None},

    # ── EUROPA OCCIDENTAL ─────────────────────────────────────────
    "Alemania":           {"iso2":"DE","iso3":"DEU","region":"europe","currency":"EUR","fx_pair":"EURUSD=X"},
    "Austria":            {"iso2":"AT","iso3":"AUT","region":"europe","currency":"EUR","fx_pair":"EURUSD=X"},
    "Belgica":            {"iso2":"BE","iso3":"BEL","region":"europe","currency":"EUR","fx_pair":"EURUSD=X"},
    "Dinamarca":          {"iso2":"DK","iso3":"DNK","region":"europe","currency":"DKK","fx_pair":"DKKUSD=X"},
    "Espana":             {"iso2":"ES","iso3":"ESP","region":"europe","currency":"EUR","fx_pair":"EURUSD=X"},
    "Finlandia":          {"iso2":"FI","iso3":"FIN","region":"europe","currency":"EUR","fx_pair":"EURUSD=X"},
    "Francia":            {"iso2":"FR","iso3":"FRA","region":"europe","currency":"EUR","fx_pair":"EURUSD=X"},
    "Grecia":             {"iso2":"GR","iso3":"GRC","region":"europe","currency":"EUR","fx_pair":"EURUSD=X"},
    "Irlanda":            {"iso2":"IE","iso3":"IRL","region":"europe","currency":"EUR","fx_pair":"EURUSD=X"},
    "Italia":             {"iso2":"IT","iso3":"ITA","region":"europe","currency":"EUR","fx_pair":"EURUSD=X"},
    "Luxemburgo":         {"iso2":"LU","iso3":"LUX","region":"europe","currency":"EUR","fx_pair":"EURUSD=X"},
    "Noruega":            {"iso2":"NO","iso3":"NOR","region":"europe","currency":"NOK","fx_pair":"NOKUSD=X"},
    "Paises Bajos":       {"iso2":"NL","iso3":"NLD","region":"europe","currency":"EUR","fx_pair":"EURUSD=X"},
    "Portugal":           {"iso2":"PT","iso3":"PRT","region":"europe","currency":"EUR","fx_pair":"EURUSD=X"},
    "Reino Unido":        {"iso2":"GB","iso3":"GBR","region":"europe","currency":"GBP","fx_pair":"GBPUSD=X"},
    "Suecia":             {"iso2":"SE","iso3":"SWE","region":"europe","currency":"SEK","fx_pair":"SEKUSD=X"},
    "Suiza":              {"iso2":"CH","iso3":"CHE","region":"europe","currency":"CHF","fx_pair":"CHFUSD=X"},

    # ── EUROPA CENTRAL Y DEL ESTE ─────────────────────────────────
    "Bulgaria":           {"iso2":"BG","iso3":"BGR","region":"europe","currency":"BGN","fx_pair":"BGNUSD=X"},
    "Croacia":            {"iso2":"HR","iso3":"HRV","region":"europe","currency":"EUR","fx_pair":"EURUSD=X"},
    "Eslovaquia":         {"iso2":"SK","iso3":"SVK","region":"europe","currency":"EUR","fx_pair":"EURUSD=X"},
    "Eslovenia":          {"iso2":"SI","iso3":"SVN","region":"europe","currency":"EUR","fx_pair":"EURUSD=X"},
    "Estonia":            {"iso2":"EE","iso3":"EST","region":"europe","currency":"EUR","fx_pair":"EURUSD=X"},
    "Hungria":            {"iso2":"HU","iso3":"HUN","region":"europe","currency":"HUF","fx_pair":"HUFUSD=X"},
    "Latvia":             {"iso2":"LV","iso3":"LVA","region":"europe","currency":"EUR","fx_pair":"EURUSD=X"},
    "Lituania":           {"iso2":"LT","iso3":"LTU","region":"europe","currency":"EUR","fx_pair":"EURUSD=X"},
    "Polonia":            {"iso2":"PL","iso3":"POL","region":"europe","currency":"PLN","fx_pair":"PLNUSD=X"},
    "Rep. Checa":         {"iso2":"CZ","iso3":"CZE","region":"europe","currency":"CZK","fx_pair":"CZKUSD=X"},
    "Rumania":            {"iso2":"RO","iso3":"ROU","region":"europe","currency":"RON","fx_pair":"RONUSD=X"},
    "Serbia":             {"iso2":"RS","iso3":"SRB","region":"europe","currency":"RSD","fx_pair":"RSDUSD=X"},
    "Ucrania":            {"iso2":"UA","iso3":"UKR","region":"europe","currency":"UAH","fx_pair":"UAHUSD=X"},

    # ── RUSIA Y ASIA CENTRAL ──────────────────────────────────────
    "Azerbaiyan":         {"iso2":"AZ","iso3":"AZE","region":"central_asia","currency":"AZN","fx_pair":"AZNUSD=X"},
    "Kazajistan":         {"iso2":"KZ","iso3":"KAZ","region":"central_asia","currency":"KZT","fx_pair":"KZTUSD=X"},
    "Russia":             {"iso2":"RU","iso3":"RUS","region":"europe","currency":"RUB","fx_pair":"RUBUSD=X"},
    "Turkmenistan":       {"iso2":"TM","iso3":"TKM","region":"central_asia","currency":"TMT","fx_pair":None},
    "Uzbekistan":         {"iso2":"UZ","iso3":"UZB","region":"central_asia","currency":"UZS","fx_pair":None},

    # ── MEDIO ORIENTE ─────────────────────────────────────────────
    "Arabia Saudita":     {"iso2":"SA","iso3":"SAU","region":"middle_east","currency":"SAR","fx_pair":"SARUSD=X"},
    "Emiratos Arabes":    {"iso2":"AE","iso3":"ARE","region":"middle_east","currency":"AED","fx_pair":"AEDUSD=X"},
    "Iran":               {"iso2":"IR","iso3":"IRN","region":"middle_east","currency":"IRR","fx_pair":None},
    "Iraq":               {"iso2":"IQ","iso3":"IRQ","region":"middle_east","currency":"IQD","fx_pair":"IQDUSD=X"},
    "Israel":             {"iso2":"IL","iso3":"ISR","region":"middle_east","currency":"ILS","fx_pair":"ILSUSD=X"},
    "Jordan":             {"iso2":"JO","iso3":"JOR","region":"middle_east","currency":"JOD","fx_pair":"JODUSD=X"},
    "Kuwait":             {"iso2":"KW","iso3":"KWT","region":"middle_east","currency":"KWD","fx_pair":"KWDUSD=X"},
    "Libano":             {"iso2":"LB","iso3":"LBN","region":"middle_east","currency":"LBP","fx_pair":None},
    "Oman":               {"iso2":"OM","iso3":"OMN","region":"middle_east","currency":"OMR","fx_pair":"OMRUSD=X"},
    "Qatar":              {"iso2":"QA","iso3":"QAT","region":"middle_east","currency":"QAR","fx_pair":"QARUSD=X"},
    "Siria":              {"iso2":"SY","iso3":"SYR","region":"middle_east","currency":"SYP","fx_pair":None},
    "Turquia":            {"iso2":"TR","iso3":"TUR","region":"middle_east","currency":"TRY","fx_pair":"TRYUSD=X"},
    "Yemen":              {"iso2":"YE","iso3":"YEM","region":"middle_east","currency":"YER","fx_pair":None},

    # ── ASIA DEL SUR ──────────────────────────────────────────────
    "Afghanistan":        {"iso2":"AF","iso3":"AFG","region":"asia_pacific","currency":"AFN","fx_pair":None},
    "Bangladesh":         {"iso2":"BD","iso3":"BGD","region":"asia_pacific","currency":"BDT","fx_pair":"BDTUSD=X"},
    "India":              {"iso2":"IN","iso3":"IND","region":"asia_pacific","currency":"INR","fx_pair":"INRUSD=X"},
    "Nepal":              {"iso2":"NP","iso3":"NPL","region":"asia_pacific","currency":"NPR","fx_pair":"NPRUSD=X"},
    "Pakistan":           {"iso2":"PK","iso3":"PAK","region":"asia_pacific","currency":"PKR","fx_pair":"PKRUSD=X"},
    "Sri Lanka":          {"iso2":"LK","iso3":"LKA","region":"asia_pacific","currency":"LKR","fx_pair":"LKRUSD=X"},

    # ── ASIA ORIENTAL ─────────────────────────────────────────────
    "China":              {"iso2":"CN","iso3":"CHN","region":"asia_pacific","currency":"CNY","fx_pair":"CNYUSD=X"},
    "Corea del Norte":    {"iso2":"KP","iso3":"PRK","region":"asia_pacific","currency":"KPW","fx_pair":None},
    "Corea del Sur":      {"iso2":"KR","iso3":"KOR","region":"asia_pacific","currency":"KRW","fx_pair":"KRWUSD=X"},
    "Japon":              {"iso2":"JP","iso3":"JPN","region":"asia_pacific","currency":"JPY","fx_pair":"JPYUSD=X"},
    "Mongolia":           {"iso2":"MN","iso3":"MNG","region":"asia_pacific","currency":"MNT","fx_pair":"MNTUSD=X"},
    "Taiwan":             {"iso2":"TW","iso3":"TWN","region":"asia_pacific","currency":"TWD","fx_pair":"TWDUSD=X"},

    # ── ASIA DEL SURESTE ──────────────────────────────────────────
    "Birmania":           {"iso2":"MM","iso3":"MMR","region":"asia_pacific","currency":"MMK","fx_pair":None},
    "Camboya":            {"iso2":"KH","iso3":"KHM","region":"asia_pacific","currency":"KHR","fx_pair":"KHRUSD=X"},
    "Filipinas":          {"iso2":"PH","iso3":"PHL","region":"asia_pacific","currency":"PHP","fx_pair":"PHPUSD=X"},
    "Indonesia":          {"iso2":"ID","iso3":"IDN","region":"asia_pacific","currency":"IDR","fx_pair":"IDRUSD=X"},
    "Laos":               {"iso2":"LA","iso3":"LAO","region":"asia_pacific","currency":"LAK","fx_pair":None},
    "Malasia":            {"iso2":"MY","iso3":"MYS","region":"asia_pacific","currency":"MYR","fx_pair":"MYRUSD=X"},
    "Singapur":           {"iso2":"SG","iso3":"SGP","region":"asia_pacific","currency":"SGD","fx_pair":"SGDUSD=X"},
    "Tailandia":          {"iso2":"TH","iso3":"THA","region":"asia_pacific","currency":"THB","fx_pair":"THBUSD=X"},
    "Timor-Leste":        {"iso2":"TL","iso3":"TLS","region":"asia_pacific","currency":"USD","fx_pair":None},
    "Vietnam":            {"iso2":"VN","iso3":"VNM","region":"asia_pacific","currency":"VND","fx_pair":"VNDUSD=X"},

    # ── OCEANÍA ───────────────────────────────────────────────────
    "Australia":          {"iso2":"AU","iso3":"AUS","region":"asia_pacific","currency":"AUD","fx_pair":"AUDUSD=X"},
    "Nueva Zelanda":      {"iso2":"NZ","iso3":"NZL","region":"asia_pacific","currency":"NZD","fx_pair":"NZDUSD=X"},
    "Papua Nueva Guinea": {"iso2":"PG","iso3":"PNG","region":"asia_pacific","currency":"PGK","fx_pair":"PGKUSD=X"},

    # ── AFRICA DEL NORTE ──────────────────────────────────────────
    "Argelia":            {"iso2":"DZ","iso3":"DZA","region":"africa","currency":"DZD","fx_pair":"DZDUSD=X"},
    "Egipto":             {"iso2":"EG","iso3":"EGY","region":"africa","currency":"EGP","fx_pair":"EGPUSD=X"},
    "Libia":              {"iso2":"LY","iso3":"LBY","region":"africa","currency":"LYD","fx_pair":None},
    "Marruecos":          {"iso2":"MA","iso3":"MAR","region":"africa","currency":"MAD","fx_pair":"MADUSD=X"},
    "Sudan":              {"iso2":"SD","iso3":"SDN","region":"africa","currency":"SDG","fx_pair":None},
    "Tunez":              {"iso2":"TN","iso3":"TUN","region":"africa","currency":"TND","fx_pair":"TNDUSD=X"},

    # ── AFRICA SUBSAHARIANA ───────────────────────────────────────
    "Angola":             {"iso2":"AO","iso3":"AGO","region":"africa","currency":"AOA","fx_pair":"AOAUSD=X"},
    "Camerun":            {"iso2":"CM","iso3":"CMR","region":"africa","currency":"XAF","fx_pair":None},
    "Congo RDC":          {"iso2":"CD","iso3":"COD","region":"africa","currency":"CDF","fx_pair":None},
    "Costa de Marfil":    {"iso2":"CI","iso3":"CIV","region":"africa","currency":"XOF","fx_pair":None},
    "Etiopia":            {"iso2":"ET","iso3":"ETH","region":"africa","currency":"ETB","fx_pair":"ETBUSD=X"},
    "Ghana":              {"iso2":"GH","iso3":"GHA","region":"africa","currency":"GHS","fx_pair":"GHSUSD=X"},
    "Guinea Ecuatorial":  {"iso2":"GQ","iso3":"GNQ","region":"africa","currency":"XAF","fx_pair":None},
    "Kenya":              {"iso2":"KE","iso3":"KEN","region":"africa","currency":"KES","fx_pair":"KESUSD=X"},
    "Madagascar":         {"iso2":"MG","iso3":"MDG","region":"africa","currency":"MGA","fx_pair":None},
    "Mozambique":         {"iso2":"MZ","iso3":"MOZ","region":"africa","currency":"MZN","fx_pair":"MZNUSD=X"},
    "Nigeria":            {"iso2":"NG","iso3":"NGA","region":"africa","currency":"NGN","fx_pair":"NGNUSD=X"},
    "Rwanda":             {"iso2":"RW","iso3":"RWA","region":"africa","currency":"RWF","fx_pair":None},
    "Senegal":            {"iso2":"SN","iso3":"SEN","region":"africa","currency":"XOF","fx_pair":None},
    "Sudafrica":          {"iso2":"ZA","iso3":"ZAF","region":"africa","currency":"ZAR","fx_pair":"ZARUSD=X"},
    "Tanzania":           {"iso2":"TZ","iso3":"TZA","region":"africa","currency":"TZS","fx_pair":"TZSUSD=X"},
    "Uganda":             {"iso2":"UG","iso3":"UGA","region":"africa","currency":"UGX","fx_pair":"UGXUSD=X"},
    "Zambia":             {"iso2":"ZM","iso3":"ZMB","region":"africa","currency":"ZMW","fx_pair":"ZMWUSD=X"},
    "Zimbabwe":           {"iso2":"ZW","iso3":"ZWE","region":"africa","currency":"ZWL","fx_pair":None},
}

# ISO3 → nombre del país (para el mapa)
ISO3_TO_NAME = {v["iso3"]: k for k, v in ALL_COUNTRIES.items()}

# ISO2 → nombre del país
ISO2_TO_NAME = {v["iso2"]: k for k, v in ALL_COUNTRIES.items()}

def get_country(name: str) -> dict:
    if name not in ALL_COUNTRIES:
        raise ValueError(
            f"País '{name}' no encontrado. "
            f"Disponibles: {list(ALL_COUNTRIES.keys())}"
        )
    return ALL_COUNTRIES[name]

def get_by_iso3(iso3: str) -> tuple:
    """Retorna (nombre, datos) por código ISO3."""
    name = ISO3_TO_NAME.get(iso3)
    if name:
        return name, ALL_COUNTRIES[name]
    return None, None
