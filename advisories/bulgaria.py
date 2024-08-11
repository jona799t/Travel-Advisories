from advisories.imports import *

ISO = "BGR"

def travel_advise(): # Data from: https://www.mfa.bg/bg/situationcenter
    html = BeautifulSoup(requests.get("https://www.mfa.bg/bg/situationcenter").text, "html.parser")

    countries = []
    for row in html.find_all("div", {"class": "col-md-6 column"}):
        for country in row.find_all("div", {"class": "row"}):
            a = country.find("div", {"class": "col-sm-6 col-xs-12 c-name"}).find("a")
            countryName = translator.translateCountryName(urllib.parse.unquote_plus(a.get("href").split("/")[-1]).title(), country="Bulgaria", language="English")
            if countryName != "ignore":
                countryAdvice = {"ISO_A3": countryName, "rating": translator.translateRating(a.get("class")[1], country="Bulgaria"), "source": "https://www.mfa.bg/bg/situationcenter"}
                countries.append(countryAdvice)

    return countries