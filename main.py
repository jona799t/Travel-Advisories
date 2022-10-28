import travel_advisories
import json

try:
    travelAdvisories = json.loads(open("travel_advisories.json").read())
except FileNotFoundError:
    open("travel_advisories.json", "w").write("{\n\n}")
    travelAdvisories = json.loads(open("travel_advisories.json").read())

travelAdvisories["denmark"] = travel_advisories.denmark()
open("travel_advisories.json", "w").write(json.dumps(travelAdvisories, indent=4))

