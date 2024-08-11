from advisories.imports import *

ISO = "DNK"

def travel_advise(): # Data from: https://um.dk/
    soup = BeautifulSoup(requests.get("https://um.dk/rejse-og-ophold/rejse-til-udlandet/rejsevejledninger").text, "html.parser")

    countries = []
    for country in soup.find("div", {"class": "dropdown-container"}).find_all("option")[1:]:
        resp = requests.get("https://um.dk" + country.get("value").replace("https://um.dk", ""))
        iso = translator.translateCountryName(country.text, country="Denmark", language="Danish")
        if "module-travel-advice-minimal" in resp.text:
            countries.append({"ISO_A3": iso, "rating": "green", "source": resp.url})
            print(countries[-1])
        elif "module-travel-advice-low" in resp.text:
            countries.append({"ISO_A3": iso, "rating": "yellow", "source": resp.url})
            print(countries[-1])
        elif "module-travel-advice-medium" in resp.text:
            countries.append({"ISO_A3": iso, "rating": "orange", "source": resp.url})
            print(countries[-1])
        elif "module-travel-advice-high" in resp.text:
            countries.append({"ISO_A3": iso, "rating": "red", "source": resp.url})
            print(countries[-1])
        else:
            countries.append({"ISO_A3": iso, "rating": None, "source": resp.url})
            print(countries[-1])

    return countries