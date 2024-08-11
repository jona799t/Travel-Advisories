from advisories.imports import *

ISO = "FIN"

def travel_advise(): # Data from: https://um.fi/matkustustiedotteet-a-o
    html = BeautifulSoup(requests.get("https://um.fi/matkustustiedotteet-a-o").text, "html.parser")

    countries = []
    for div in html.find_all("div", {"class": "item span-row"}):
        countryName = translator.translateCountryName(div.find("a").text.replace(": matkustustiedote", ""), country="Finland", language="Finnish")
        if countryName != "ignore":
            countryAdvice = {"ISO_A3": countryName, "rating": translator.translateRating(div.find("p").text, country="Finland"), "source": "https://um.fi/matkustustiedotteet-a-o"}
            countries.append(countryAdvice)

    return countries