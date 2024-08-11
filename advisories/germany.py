from advisories.imports import *

ISO = "DEU"

def travel_advise(): # Data from: https://www.auswaertiges-amt.de/de/ReiseUndSicherheit/10.2.8Reisewarnungen
    html = BeautifulSoup(requests.get("https://www.auswaertiges-amt.de/de/ReiseUndSicherheit/10.2.8Reisewarnungen").text, "html.parser")

    countries = []
    for li in html.find_all("li", {"class": "rte__list-item"}):
        countryData = li.text.lstrip().split(": ")
        countryName = translator.translateCountryName(countryData[0], country="Germany", language="German")
        if countryName != "ignore":
            countryAdvice = {"ISO_A3": countryName, "rating": translator.translateRating(countryData[1].split("(")[-1].replace(")", ""), country="Germany"), "source": "https://www.auswaertiges-amt.de/de/ReiseUndSicherheit/10.2.8Reisewarnungen"}
            countries.append(countryAdvice)
    return countries