from advisories.imports import *

ISO = "HRV"

def travel_advise(): # Data from: https://mvep.gov.hr/default.aspx?id=245044
    html = BeautifulSoup(requests.get("https://mvep.gov.hr/default.aspx?id=245044").text, "html.parser")
    countries = []
    for option in html.find_all("select")[1].find_all("option"):
        countryName = translator.translateCountryName(option.text.lstrip(), country="Croatia", language="Croatian")
        if countryName != "ignore":
            countryHtml = BeautifulSoup(requests.post(f"https://mvep.gov.hr/default.aspx?id=245044&country={option.get('value')}").text, "html.parser")
            countryAdvice = {"ISO_A3": countryName, "rating": translator.translateRating(countryHtml.find("div", {"class": "page_content"}).find("li").text, country="Croatia"), "source": f"https://mvep.gov.hr/default.aspx?id=245044&country={option.get('value')}"}
            countries.append(countryAdvice)
            print(countryAdvice)

    return countries