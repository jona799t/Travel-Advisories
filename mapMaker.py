from advisories import australia, austria, bulgaria, canada, croatia, denmark, finland, germany, hongkong, hungary, indonesia, ireland, united_states
import json
import os

travel_advisories = [austria, bulgaria, canada, croatia, denmark, hongkong, hungary, indonesia, ireland, united_states]
advise = {}
for travel_advisory in travel_advisories:
    advise[travel_advisory.ISO] = {}
    for country_advise in travel_advisory.travel_advise():
        advise[travel_advisory.ISO][country_advise["ISO_A3"]] = country_advise

countries = json.loads(open("templates/countries.json").read())
alpha3To2 = {}
for country in countries:
    alpha3To2[country["alpha3"].lower()] = country["alpha2"].lower()
print(alpha3To2)

for country, advise in advise.items():
    map = open("templates/BlankMap-World.svg").read()
    countries = {
        "green": [],
        "yellow": [],
        "orange": [],
        "red": [],
        None: []
    }
    for countryAdviced, countryAdvice in advise.items():
        print(country, countryAdviced, countryAdvice)
        if countryAdviced != "-99":
            countries[countryAdvice["rating"]].append(alpha3To2[countryAdviced.lower()])

    svgEdit = "\n"
    svgEdit += f"        .{', .'.join(countries['green'])}" + "\n        {\n            fill: #007C4F;\n        }\n"""
    svgEdit += f"        .{', .'.join(countries['yellow'])}" + "\n        {\n            fill: #FED42B;\n        }\n"""
    svgEdit += f"        .{', .'.join(countries['orange'])}" + "\n        {\n            fill: #FF8800;\n        }\n"""
    svgEdit += f"        .{', .'.join(countries['red'])}" + "\n        {\n            fill: #EE0000;\n        }\n"""
    svgEdit += f"        .{alpha3To2[country.lower()]}" + "\n        {\n            fill: #001E78;\n        }\n"""

    map = map.replace("""        /*
         * Travel advisory
         */""", """        /*
         * Travel advisory
         */""" + svgEdit)

    if not os.path.exists("maps"):
        os.makedirs("maps")

    open(f"maps/{country}.svg", "w").write(map)
