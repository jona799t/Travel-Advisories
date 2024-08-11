from advisories.imports import *

ISO = "IDN"

def travel_advise(): # Data from: https://safetravel.kemlu.go.id/country-info
    resp = requests.get("https://safetravel.kemlu.go.id/api/country-info", verify=False)

    countries = []
    for country in resp.json():
        countryName = translator.translateCountryName(country["country_name"], country="Indonesia", language="Indonesian")
        if countryName != "ignore":
            countryAdvice = {"ISO_A3": countryName, "rating": translator.translateRating(country["country_indicator"], country="Indonesia"), "source": "https://safetravel.kemlu.go.id/api/country-info"}
            countries.append(countryAdvice)
            print(countryAdvice)

    return countries