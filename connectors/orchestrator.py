# connectors/orchestrator.py
from datetime import datetime
from data.all_countries import get_country
from connectors import world_bank, imf, yahoo_finance

def fetch_automatic_data(country_name: str) -> dict:
    country      = get_country(country_name)
    iso2         = country["iso2"]
    fx_pair      = country.get("fx_pair")
    current_year = datetime.now().year

    wb_data  = world_bank.fetch_all(iso2)
    imf_data = imf.fetch_all(iso2)

    volatility = yahoo_finance.fetch_fx_volatility(fx_pair)
    fx_current = yahoo_finance.fetch_fx_current(fx_pair)
    fx_range   = yahoo_finance.fetch_fx_range_12m(fx_pair)

    fx_entry = {"value": volatility, "year": current_year, "source": "Yahoo Finance"}

    all_data = {**wb_data, **imf_data, "ECO_07": fx_entry}
    all_data["_fx_pair"]    = fx_pair
    all_data["_fx_current"] = fx_current
    all_data["_fx_range"]   = fx_range
    return all_data
