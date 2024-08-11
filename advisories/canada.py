from advisories.imports import *

ISO = "CAN"

def travel_advise(): # Data from: https://travel.gc.ca/travelling/advisories
    html = BeautifulSoup(requests.get("https://travel.gc.ca/travelling/advisories").text, "html.parser")

    countries = []
    for row in html.find("tbody").find_all("tr"):
        countryName = translator.translateCountryName(row.find("a").text, "Canada", "English")
        if countryName != "ignore":
            countryAdvise = {"ISO_A3": countryName, "rating": translator.translateRating(row.find("img").get("class")[0], country="Canada"), "source": "https://travel.gc.ca/travelling/advisories"}
            countries.append(countryAdvise)
            print(countryAdvise)

    return countries