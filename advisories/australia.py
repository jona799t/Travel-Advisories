from advisories.imports import *

ISO = "AUS"

def travel_advise(): # Data from: https://smartraveller.gov.au/
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
                countryAdvice = {"ISO_A3": countryName, "rating": translator.translateRating(country[3].replace("          ", ""), country="Australia"), "source": "https://www.smartraveller.gov.au/destinations"}
                countries.append(countryAdvice)

    return countries