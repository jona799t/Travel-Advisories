import os
import json

from copy import deepcopy
from translate import Translator

path = os.path.abspath(__name__).replace(".translator", "")
dictionary = json.loads(open(path + "/dictionary.json").read())

def translateCountryName(countryName, country, language):
    try:
        dictionary[country.lower()]
    except KeyError:
        makeEntry = input(f"The country: {country} could not be found. Do you want to make an entry for it? (y/n): ")
        if makeEntry == "y":
            dictionary[country.lower()] = {}
        elif makeEntry != "n":
            raise Exception("Option not found")

    try:
        dictionary[country.lower()]["countries"]
    except Exception:
        dictionary[country.lower()]["countries"] = {}

    if countryName in dictionary[country.lower()]["countries"]:
        return dictionary[country.lower()]["countries"][countryName]

    else:
        if language.lower() != "english":
            translator = Translator(from_lang=language, to_lang="english")

        success = False
        try:
            if language.lower() != "english" and (_countryTranslated := translator.translate(countryName)) in dictionary["general"]["countries"]:
                countryTranslated = _countryTranslated
                success = True
        except Exception:
            name = input(f"What should {countryName} be translated to? (Click enter to ignore it): ")
            if name == "":
                countryTranslated = "ignore"
            else:
                if name in dictionary["general"]["countries"]:
                    countryTranslated = name
                else:
                    print(f"{name} could not be found in the database. Ignoring")
                    countryTranslated = "ignore"
            success = True


        if not success and language.lower() == "english" and countryName in dictionary["general"]["countries"]:
            countryTranslated = countryName
        elif not success:
            name = input(f"What should {countryName} be translated to? (Click enter to ignore it): ")
            if name == "":
                countryTranslated = "ignore"
            else:
                if name in dictionary["general"]["countries"]:
                    countryTranslated = name
                else:
                    print(f"{name} could not be found in the database. Ignoring")
                    countryTranslated = "ignore"

        dictionary[country.lower()]["countries"][countryName] = countryTranslated
        open(path + "/dictionary.json", "w").write(json.dumps(dictionary, indent=4))

    return countryTranslated

def translateRating(rating, country):
    global dictionary

    rating = str(rating)
    try:
        dictionary[country.lower()]
    except KeyError:
        makeEntry = input(f"The country: {country} could not be found. Do you want to make an entry for it? (y/n) ")
        if makeEntry == "y":
            dictionary[country.lower()] = {}
        elif makeEntry != "n":
            raise Exception("Option not found")

    try:
        dictionary[country.lower()]["travel_advice"]
    except Exception:
        dictionary[country.lower()]["travel_advice"] = {}

    try:
        dictionary[country.lower()]["travel_advice"][rating]
    except KeyError:
        _rating = int(input(f"""Should {rating} be
1: Green
2: Yellow
3: Orange
4: Red

5: None
?: """))
        if _rating == 1: dictionary[country.lower()]["travel_advice"][rating] = "green"
        elif _rating == 2: dictionary[country.lower()]["travel_advice"][rating] = "yellow"
        elif _rating == 3: dictionary[country.lower()]["travel_advice"][rating] = "orange"
        elif _rating == 4: dictionary[country.lower()]["travel_advice"][rating] = "red"
        elif _rating == 5: dictionary[country.lower()]["travel_advice"][rating] = None
        else: raise Exception("Option not found")


        tempDictionary = deepcopy(dictionary)
        tempDictionary[country.lower()] = {}
        tempDictionary[country.lower()]["travel_advice"] = dictionary[country.lower()]["travel_advice"]
        tempDictionary[country.lower()]["countries"] = dictionary[country.lower()]["countries"]
        dictionary = tempDictionary

        open(path + "/dictionary.json", "w").write(json.dumps(dictionary, indent=4))
        dictionary = json.loads(open(path + "/dictionary.json").read())

    try:
        return dictionary[country.lower()]["travel_advice"][rating]
    except Exception:
        print("Failed to translate rating")
        return rating