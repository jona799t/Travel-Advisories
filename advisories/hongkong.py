from advisories.imports import *

ISO = "HKG"

def travel_advise(): # Data from: https://www.sb.gov.hk
    resp = requests.get("https://www.sb.gov.hk/json/ota_index/ota_index_2022.json")

    countries = []
    for element in resp.json()["otas"]:
        for country in element["countries"]:
            countryName = translator.translateCountryName(country["titleEn"], country="Hong Kong", language="English")
            if countryName != "ignore":
                countryAdvice = {"ISO_A3": countryName, "rating": translator.translateRating(element["level"], country="Hong Kong"), "source": "https://www.sb.gov.hk/json/ota_index/ota_index_2022.json"}
                countries.append(countryAdvice)
                print(countryAdvice)

    return countries