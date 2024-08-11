from advisories import australia, austria, bulgaria, canada, croatia, denmark, finland, germany, hongkong, hungary, indonesia, ireland, united_states
import json

travel_advisories = [indonesia, ireland, united_states]
advise = {}
for travel_advisory in travel_advisories:
    advise[travel_advisory.ISO] = {}
    for country_advise in travel_advisory.travel_advise():
        advise[travel_advisory.ISO][country_advise["ISO_A3"]] = country_advise

print(json.dumps(advise))