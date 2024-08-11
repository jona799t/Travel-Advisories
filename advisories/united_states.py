from advisories.imports import *

ISO = "USA"

def travel_advise(): # Data from: https://travel.state.gov/content/travel/en/traveladvisories/traveladvisories.html/
    soup = BeautifulSoup(requests.get("https://travel.state.gov/content/travel/en/traveladvisories/traveladvisories.html/").text, "html.parser")
    advise = []
    for country in soup.find_all("tr")[1:]:
        tds = country.find_all("td")
        countryName = translator.translateCountryName(tds[0].text.replace(" Travel Advisory", "").strip(), country="United States", language="English")
        if countryName != "ignore":
            if tds[1].text == "Other":
                pass # Mangler
            countryAdvice = {"ISO_A3": countryName, "rating": translator.translateRating(tds[1].text, country="United States"), "source": "https://travel.state.gov/content/travel/en/traveladvisories/traveladvisories.html/"}
            advise.append(countryAdvice)

    return advise