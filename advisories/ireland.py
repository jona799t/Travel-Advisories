from advisories.imports import *

ISO = "IRL"

def travel_advise(): # Data from: https://www.dfa.ie/travel/travel-advice/
    html = BeautifulSoup(requests.get("https://www.dfa.ie/travel/travel-advice/").text, "html.parser")

    countries = []
    for a in html.find_all("a"):
        if "/travel/travel-advice/a-z-list-of-countries/" in (travelAdvice := str(a.get("href"))) and a.get("class") == None:
            countryName = translator.translateCountryName(a.text.replace("\n", ""), country="Ireland", language="English")
            if countryName != "ignore":
                countryAdvice = {"ISO_A3": countryName, "rating": translator.translateRating(BeautifulSoup(requests.get("https://www.dfa.ie" + travelAdvice).text, "html.parser").find("section", {"class": "security-status"}).get("class")[-1], country="Ireland"), "source": "https://www.dfa.ie" + travelAdvice}
                countries.append(countryAdvice)
                print(countryAdvice)

    return countries