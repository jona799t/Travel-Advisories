from advisories.imports import *

ISO = "HUN"

def travel_advise(): # Data from: https://konzinfo.mfa.gov.hu/utazas/utazasi-tanacsok-orszagonkent
    html = BeautifulSoup(requests.get("https://konzinfo.mfa.gov.hu/utazas/utazasi-tanacsok-orszagonkent").text, "html.parser")

    countries = []
    for a in html.find_all("a", {"class": "dropdown-item use-ajax"}):
        countryName = translator.translateCountryName(a.text, country="Hungary", language="Hungarian")
        if countryName != "ignore":
            url = "https://konzinfo.mfa.gov.hu" + BeautifulSoup(requests.get("https://konzinfo.mfa.gov.hu" + a.get("href")).json()[0]["data"], "html.parser").find("a").get("href")
            countryHtml = BeautifulSoup(requests.get(url).text, "html.parser")
            countryAdvice = {"ISO_A3": countryName, "rating": translator.translateRating(countryHtml.find("img", {"class": "image-style-ikon-40"}).get("alt"), country="Hungary"), "source": url}
            countries.append(countryAdvice)
            print(countryAdvice)

    return countries