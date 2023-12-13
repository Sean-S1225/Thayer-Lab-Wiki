from collections import callable
import os
import json

def GetDirectories(path: str) -> list[str]:
    """Gets all directories in the user-uploaded section. This is the first step,
    more logic will follow to verify the data contained"""
    
    directories = []
    for x in os.listdir(path):
        if os.path.isdir((dir := os.join(path, x))):
            directories.append(dir)

    return directories

def GetJSONFiles(directories: list[str], jsonName: str) -> list[dict]:
    """Gets all .json files associated with user uploaded scripts"""
    
    jsonDicts = []
    for dir in directories:
        if os.path.isfile((file := os.path.join(dir, jsonName))):
            with open(file, "r") as f:
                jsonDicts.append(json.load(f))

    return jsonDicts


def CheckJSONFiles(jsonDicts: list[dict], requiredFields: list[str]) -> list[dict]:
    """Returns the .json dictionaries that have all of the required fields"""

    for d in jsonDicts:
        for field in requiredFields:
            if field not in d:
                jsonDicts.remove(d)
    
    return jsonDicts


def VerifyFields(jsonDicts: list[dict], verify: dict[str, callable[[str], bool]]) -> list[dict]:
    """Returns the .json dictionaries that pass some sort of verification on a specific field"""

    for d in jsonDicts:
        for key, check in verify.items():
            if not check(d[key]):
                jsonDicts.remove(d)

    return jsonDicts

def CheckDate(date: str) -> bool:
    """Ensures a date is in the following format: "[Month] [day] [year]", where the first letter of the full
    month name is capitalized, the full four-number year is given, and there are no commas or any other characters.

    Args:
        date: The string to check

    Returns:
        True if the date is in the correct format, False otherwise
    """
    date = date.split(" ")
    if not len(date) == 3:
        return False
    
    months = ["January", "February", "March", "April", "May", "June", "July",
              "August", "September", "October", "November", "December"]
    
    return date[0] in months and str.isdigit(date[1]) and int(date[1]) <= 31 and len(str(date[2])) == 4

def GetValidJSONFiles(path: str, jsonName: str, requiredFields: list[str], verify: dict[str, callable[[str], bool]]) -> list[dict]:
    """Implements all of the above functions in one fantastic line :)"""
    return VerifyFields(CheckJSONFiles(GetJSONFiles(GetDirectories(path), jsonName), requiredFields), verify)