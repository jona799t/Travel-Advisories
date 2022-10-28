import requests
import json
import re
from bs4 import BeautifulSoup
import urllib.parse
import os
from travel_advisories import translator

# Travel Advisories sites can be found on: https://en.wikipedia.org/wiki/Travel_warning

def australia(): # Data from: https://smartraveller.gov.au/
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-DK,en;q=0.9,da-DK;q=0.8,da;q=0.7,en-US;q=0.6',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36',
    }
    html = BeautifulSoup(requests.get("https://www.smartraveller.gov.au/destinations", headers=headers).text, "html.parser")

    countries = []
    for country in html.find_all("tr"):
        if "views-field views-field-title" in str(country) and "No travel advice" not in country.text and "Destinatio" not in country.text:
            country = country.text.split("\n")
            countryName = translator.translateCountryName(country[1][:-1], country="Australia", language="English")
            if countryName != "ignore":
                countryAdvice = {
                    "name": translator.translateCountryName(country[1][:-1], country="Australia", language="English"),
                    "travel_advice": translator.translateRating(country[3].replace("          ", ""), country="Australia")
                }
                print(countryAdvice)
                countries.append(countryAdvice)

    return countries

def austria(): # Data from: https://bmeia.gv.at/
    html = BeautifulSoup(requests.get("https://www.bmeia.gv.at/reise-services/laender/").text, "html.parser")

    countries = []
    _countries = []
    for country in html.find_all("li", {"class": "dontsplit"}):
        if (country := country.find("a")).text != " " and country.text not in _countries:
            _countries.append(country.text)
            countryName = translator.translateCountryName(country.text[1:-1], country="Austria", language="German")
            if countryName == "ignore":
                break
            countries.append({
                "name": countryName,
                "url": "https://bmeia.gv.at" + country.get("href"),
                "travel_advice": None
            })

    i = 0
    for country in countries:
        if "Überseegebiete" not in country["name"]:
            try:
                securityLevel = re.findall("Sicherheitsstufe [1-6]", requests.get(country["url"]).text)
                country["travel_advice"] = translator.translateRating(sorted(securityLevel)[0], country="Austria")

            except Exception:
                print(f"Deleting: {countries[i]['name']}")
                del countries[i]
        else:
            del countries[i]

        del country["url"]

        i += 1
        print(country)

    return countries

def belgium(): # Data from: https://diplomatie.belgium.be/fr/pays
    raise Exception("The data on the belgium travel advisory site is not consistent enough to support it")

def bulgaria(): # Data from: https://www.mfa.bg/bg/situationcenter
    html = BeautifulSoup(requests.get("https://www.mfa.bg/bg/situationcenter").text, "html.parser")

    countries = []
    for row in html.find_all("div", {"class": "col-md-6 column"}):
        for country in row.find_all("div", {"class": "row"}):
            a = country.find("div", {"class": "col-sm-6 col-xs-12 c-name"}).find("a")
            countryName = translator.translateCountryName(urllib.parse.unquote_plus(a.get("href").split("/")[-1]).title(), country="Bulgaria", language="English")
            if countryName != "ignore":
                countryAdvise = {
                    "name": countryName,
                    "travel_advice": translator.translateRating(a.get("class")[1], country="Bulgaria")
                }
                countries.append(countryAdvise)
                print(countryAdvise)

    return countries

def canada(): # Data from: https://travel.gc.ca/travelling/advisories
    html = BeautifulSoup(requests.get("https://travel.gc.ca/travelling/advisories").text, "html.parser")

    countries = []
    for row in html.find("tbody").find_all("tr"):
        countryName = translator.translateCountryName(row.find("a").text, "Canada", "English")
        if countryName != "ignore":
            countryAdvise = {
                "name": countryName,
                "travel_advice": translator.translateRating(row.find("img").get("class")[0], country="Canada")
            }
            countries.append(countryAdvise)
            print(countryAdvise)

    return countries

def croatia(): # Data from: https://mvep.gov.hr/default.aspx?id=245044
    html = BeautifulSoup(requests.get("https://mvep.gov.hr/default.aspx?id=245044").text, "html.parser")
    countries = []
    for option in html.find_all("select")[1].find_all("option"):
        countryName = translator.translateCountryName(option.text.lstrip(), country="Croatia", language="Croatian")
        if countryName != "ignore":
            countryHtml = BeautifulSoup(requests.post(f"https://mvep.gov.hr/default.aspx?id=245044&country={option.get('value')}").text, "html.parser")
            countryAdvice = {
                "name": countryName,
                "travel_advice": translator.translateRating(countryHtml.find("div", {"class": "page_content"}).find("li").text, country="Croatia")
            }
            countries.append(countryAdvice)
            print(countryAdvice)

    return countries

def cyprus(): # Data from: https://mfa.gov.cy/advice/
    raise Exception("At the time only 3 countries has been added")

def czech_republic(): # Data from: https://www.mzv.cz/jnp/cz/cestujeme/aktualni_doporuceni_a_varovani/index.html
    raise Exception("At the time this function is not usable")

def denmark(): # Data from: https://um.dk/
    html = BeautifulSoup(requests.get("https://um.dk/rejse-og-ophold/rejse-til-udlandet/rejsevejledninger").text, "html.parser")

    countries = []
    for country in html.find("div", {"class": "dropdown-container"}).find_all("option"):
        if country.get("title") != "" and country.get("title") != "\n" and country.get("value") != "":
            countryName = translator.translateCountryName(country.text, country="Denmark", language="Danish")
            if countryName == "ignore":
                break
            countries.append({"name": countryName, "url": "https://um.dk" + country.get("value").replace("https://um.dk", ""), "travel_advice": None})

    for country in countries:
        html = BeautifulSoup(requests.get(country["url"]).text, "html.parser")
        for h2 in html.find_all("h2"):
            _break = False
            try:
                if "module-travel-advice" in (_class := h2.get("class")[0]):
                    country["travel_advice"] = translator.translateRating(_class, country="Denmark")
                    _break = True
            except Exception:
                pass

            if _break:
                break

        del country['url']
        print(country)

    return countries

def estonia(): # Data from: https://vm.ee/et/riigid/reisiinfo
    raise Exception("At the time this function is not usable")

def finland(): # Data from: https://um.fi/matkustustiedotteet-a-o
    html = BeautifulSoup(requests.get("https://um.fi/matkustustiedotteet-a-o").text, "html.parser")

    countries = []
    for div in html.find_all("div", {"class": "item span-row"}):
        countryName = translator.translateCountryName(div.find("a").text.replace(": matkustustiedote", ""), country="Finland", language="Finnish")
        if countryName != "ignore":
            countryAdvise = {
                "name": countryName,
                "travel_advice": translator.translateRating(div.find("p").text, country="Finland")
            }
            print(countryAdvise)
            countries.append(countryAdvise)

    return countries

def germany(): # Data from: https://www.auswaertiges-amt.de/de/ReiseUndSicherheit/10.2.8Reisewarnungen
    html = BeautifulSoup(requests.get("https://www.auswaertiges-amt.de/de/ReiseUndSicherheit/10.2.8Reisewarnungen").text, "html.parser")

    countries = []
    for li in html.find_all("li", {"class": "rte__list-item"}):
        countryData = li.text.lstrip().split(": ")
        countryName = translator.translateCountryName(countryData[0], country="Germany", language="German")
        if countryName != "ignore":
            countryAdvice = {
                "name": countryName,
                "travel_advice": translator.translateRating(countryData[1].split("(")[1].replace(") ", ""), country="Germany")
            }
            print(countryAdvice)
            countries.append(countryAdvice)
    return countries

def hongkong(): # Data from: https://www.sb.gov.hk/eng/ota/index.html
    resp = requests.get("https://www.sb.gov.hk/json/ota_index/ota_index_2022.json")

    countries = []
    for element in resp.json()["otas"]:
        for country in element["countries"]:
            countryName = translator.translateCountryName(country["titleEn"], country="Hong Kong", language="English")
            if countryName != "ignore":
                countryAdvice = {
                    "name": countryName,
                    "travel_advice": translator.translateRating(element["level"], country="Hong Kong")
                }
                countries.append(countryAdvice)
                print(countryAdvice)

    return countries

def hungary(): # Data from: https://konzinfo.mfa.gov.hu/utazas/utazasi-tanacsok-orszagonkent
    html = BeautifulSoup(requests.get("https://konzinfo.mfa.gov.hu/utazas/utazasi-tanacsok-orszagonkent").text, "html.parser")

    countries = []
    for a in html.find_all("a", {"class": "dropdown-item use-ajax"}):
        countryName = translator.translateCountryName(a.text, country="Hungary", language="Hungarian")
        if countryName != "ignore":
            countryHtml = BeautifulSoup(requests.get("https://konzinfo.mfa.gov.hu" + BeautifulSoup(requests.get("https://konzinfo.mfa.gov.hu" + a.get("href")).json()[0]["data"], "html.parser").find("a").get("href")).text, "html.parser")
            countryAdvise = {
                "name": countryName,
                "travel_advice": translator.translateRating(countryHtml.find("img", {"class": "image-style-ikon-40"}).get("alt"), country="Hungary")
            }
            countries.append(countryAdvise)
            print(countryAdvise)

    return countries

def india(): # Data from: https://mea.gov.in/travel-advisories.htm
    raise Exception("The website is to unstructured")

def indonesia(): # Data from: https://safetravel.kemlu.go.id/country-info
    resp = requests.get("https://safetravel.kemlu.go.id/api/country-info")

    countries = []
    for country in resp.json():
        countryName = translator.translateCountryName(country["country_name"], country="Indonesia", language="Indonesian")
        if countryName != "ignore":
            countryAdvice = {
                "name": countryName,
                "travel_advice": translator.translateRating(country["country_indicator"], country="Indonesia")
            }
            countries.append(countryAdvice)
            print(countryAdvice)

    return countries

def ireland(): # Data from: https://www.dfa.ie/travel/travel-advice/
    html = BeautifulSoup(requests.get("https://www.dfa.ie/travel/travel-advice/").text, "html.parser")

    countries = []
    for a in html.find_all("a"):
        if "/travel/travel-advice/a-z-list-of-countries/" in (travelAdvice := str(a.get("href"))) and a.get("class") == None:
            countryName = translator.translateCountryName(a.text.replace("\n", ""), country="Ireland", language="English")
            if countryName != "ignore":
                countryAdvice = {
                    "name": countryName,
                    "travel_advice": translator.translateRating(BeautifulSoup(requests.get("https://www.dfa.ie" + travelAdvice).text, "html.parser").find("section", {"class": "security-status"}).get("class")[-1], country="Ireland")
                }
                countries.append(countryAdvice)
                print(countryAdvice)

    return countries