import requests
import json

wb_base_url = "http://api.worldbank.org/v2/country/all/indicator/"
wb_gdp_indicator = "NY.GDP.PCAP.CD"

wb_data_cache_file_path = "Resources/wb_data_cache.json"

def getGdpData():
    try:
        with open(wb_data_cache_file_path) as wb_data_cache_file:
            return json.load(wb_data_cache_file)
    except:
        pass

    params = {
        "format": "json"
    }
    response = requests.get(wb_base_url + wb_gdp_indicator, params).json()
    pages = response[0]["pages"]

    final_result = response[1]

    for page in range(2, pages):
        params["page"] = page
        response = requests.get(wb_base_url + wb_gdp_indicator, params).json()
        final_result += response[1]

    try:
        with open(wb_data_cache_file_path, "w") as wb_data_cache_file:
            wb_data_cache_file.write(json.dumps(final_result, indent=4))
    except:
        pass

    return final_result
