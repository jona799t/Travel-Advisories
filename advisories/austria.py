from advisories.imports import *

ISO = "AUT"

def travel_advise(): # Data from: https://bmeia.gv.at/
    html = BeautifulSoup(requests.get("https://www.bmeia.gv.at/reise-services/laender-a-bis-z").text, "html.parser")

    countries = []
    _countries = []
    for _country in html.find_all("li", {"class": "dontsplit"}):
        if (country := _country.find("a")).text != " " and country.text.strip() not in _countries:
            _countries.append(country.text.strip())
            countryName = translator.translateCountryName(country.text.strip(), country="Austria", language="German")
            if countryName == "ignore":
                continue
            countries.append({
                "name": countryName,
                "url": "https://bmeia.gv.at" + country.get("href"),
                "travel_advice": None
            })

    advise = []
    for country in countries:
        if "Überseegebiete" not in country["name"]:
            resp = requests.get(country["url"])
            securityLevel = re.findall("Sicherheitsstufe [1-6]", resp.text.replace("&nbsp;", " "))
            advise.append({"ISO_A3": country["name"], "rating": translator.translateRating(sorted(securityLevel)[0], country="Austria"), "source": country["url"]})

        print(advise[-1])

    return advise

def travel_advise_new(): # Data from: https://www.bmeia.gv.at/reise-services/reisewarnungen/
    html = BeautifulSoup(requests.get("https://www.bmeia.gv.at/reise-services/reisewarnungen/").text, "html.parser")
    map = html.find("div", {"class": "tx-bmeia-countries"})
    script = map.find("script")

    advise = []
    for countryCode, data in json.loads(re.search("var bmeiaCountrySecurityInfos = [^\n]+", script.text).group()[32:-1]).items():
        if countryCode != "0":
            countryName = translator.translateCountryName(data["title"], country="Austria", language="German")
            if countryName == "ignore":
                continue
            # The map is not updated thus the code needs to individually check each country
            resp = requests.get("https://www.bmeia.gv.at" + data["link"])
            securityLevel = re.findall("Sicherheitsstufe [1-6]", resp.text.replace("&nbsp;", " "))
            advise.append({"ISO_A3": countryName, "rating": translator.translateRating(sorted(securityLevel)[0], country="Austria"), "source": resp.url})
            print(advise[-1])

    return advise