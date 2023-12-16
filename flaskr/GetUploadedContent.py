from collections.abc import Callable
import os
import json
from sys import path
path.append("../")
import unit_test

def GetDirectories(path: str) -> list[str]:
    """Gets all directories in the user-uploaded section. This is the first step,
    more logic will follow to verify the data contained"""
    
    directories = []
    for x in os.listdir(path):
        if os.path.isdir((dir := os.path.join(path, x))):
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
                break
    
    return jsonDicts


def VerifyFields(jsonDicts: list[dict], verify: dict[str, Callable[[str], bool]]) -> list[dict]:
    """Returns the .json dictionaries that pass some sort of verification on a specific field"""

    toReturn = []

    for d in jsonDicts:
        include = True
        for key, check in verify.items():
            if not check(d[key]):
                include = False
        if include:
            toReturn.append(d)

    return toReturn

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

def GetValidJSONFiles(path: str, jsonName: str, requiredFields: list[str], verify: dict[str, Callable[[str], bool]]) -> list[dict]:
    """Implements all of the above functions in one fantastic line :)"""
    return VerifyFields(CheckJSONFiles(GetJSONFiles(GetDirectories(path), jsonName), requiredFields), verify)

if __name__ == "__main__":

    unit_test.UnitTest(GetDirectories, ("../tests/Scripts_Templates/",), 
                       (["../tests/Scripts_Templates/Correct", "../tests/Scripts_Templates/Extra", 
                        "../tests/Scripts_Templates/Missing1", "../tests/Scripts_Templates/Missing1", 
                        "../tests/Scripts_Templates/Missing2", "../tests/Scripts_Templates/WrongDate", 
                        "../tests/Scripts_Templates/WrongDate2"],), lambda x, y: set(x[0]) == set(y[0]))

    unit_test.UnitTest(GetJSONFiles, (["../tests/Scripts_Templates/Correct", "../tests/Scripts_Templates/Extra"], "Script.json"), 
                       ([{"Uploader_Name": "Sean",
                         "Created": "October 18 2023",
                         "Last_Updated": "October 19 2023",
                         "Program": "Python",
                         "Name": "Dihedral RMSD (Numba)",
                         "File_Name": "Correct/test.py",
                         "Description": "Calculates Root-Mean-Squared Deviation (RMSD) of a protein's dihedral angles"},
                        {"Uploader_Name": "Sean",
                         "Created": "October 18 2023",
                         "Last_Updated": "October 19 2023",
                         "Program": "Python",
                         "Name": "Dihedral RMSD (Numba)",
                         "File_Name": "Extra/test.py",
                         "Description": "Calculates Root-Mean-Squared Deviation (RMSD) of a protein's dihedral angles",
                         "New": "nothing!"}],))
    
    unit_test.UnitTest(GetJSONFiles, (["../tests/Scripts_Templates/WrongDate", "../tests/Scripts_Templates/WrongDate2"], "Script.json"),
                       ([{
                        "Uploader_Name": "Sean",
                        "Created": "October 18 2023",
                        "Last_Updated": "Oct 19 2023",
                        "Program": "Python",
                        "Name": "Dihedral RMSD (Numba)",
                        "File_Name": "WrongDate/test.py",
                        "Description": "Calculates Root-Mean-Squared Deviation (RMSD) of a protein's dihedral angles"
                       },
                       {
                        "Uploader_Name": "Sean",
                        "Created": "October 18 202",
                        "Last_Updated": "Oct 19 2023",
                        "Program": "Python",
                        "Name": "Dihedral RMSD (Numba)",
                        "File_Name": "WrongDate2/test.py",
                        "Description": "Calculates Root-Mean-Squared Deviation (RMSD) of a protein's dihedral angles"
                       }],))
    
    unit_test.UnitTest(CheckJSONFiles, (GetJSONFiles(["../tests/Scripts_Templates/Correct", "../tests/Scripts_Templates/Extra"], "Script.json"), 
                                        ["Uploader_Name", "Created", "Last_Updated", "Program", "Name", "File_Name", "Description"]),
                       ([{"Uploader_Name": "Sean",
                          "Created": "October 18 2023",
                          "Last_Updated": "October 19 2023",
                          "Program": "Python",
                          "Name": "Dihedral RMSD (Numba)",
                          "File_Name": "Correct/test.py",
                          "Description": "Calculates Root-Mean-Squared Deviation (RMSD) of a protein's dihedral angles"},
                        {"Uploader_Name": "Sean",
                          "Created": "October 18 2023",
                          "Last_Updated": "October 19 2023",
                          "Program": "Python",
                          "Name": "Dihedral RMSD (Numba)",
                          "File_Name": "Extra/test.py",
                          "Description": "Calculates Root-Mean-Squared Deviation (RMSD) of a protein's dihedral angles",
                          "New": "nothing!"}],))
    
    unit_test.UnitTest(VerifyFields, args=([
                        {
                        "Uploader_Name": "Sean",
                        "Created": "October 18 2023",
                        "Last_Updated": "Oct 19 2023",
                        "Program": "Python",
                        "Name": "Dihedral RMSD (Numba)",
                        "File_Name": "WrongDate/test.py",
                        "Description": "Calculates Root-Mean-Squared Deviation (RMSD) of a protein's dihedral angles"
                       },
                       {
                        "Uploader_Name": "Sean",
                        "Created": "October 18 202",
                        "Last_Updated": "Oct 19 2023",
                        "Program": "Python",
                        "Name": "Dihedral RMSD (Numba)",
                        "File_Name": "WrongDate2/test.py",
                        "Description": "Calculates Root-Mean-Squared Deviation (RMSD) of a protein's dihedral angles"
                       }],
                       {"Created": CheckDate, "Last_Updated": CheckDate}), 
                       returns=([],))


    unit_test.UnitTest(CheckDate, ("October 31 2023",), (True,))
    unit_test.UnitTest(CheckDate, ("January 1 1990",), (True,))
    unit_test.UnitTest(CheckDate, ("January -1 1990",), (False,))
    unit_test.UnitTest(CheckDate, ("March 16.5 1990",), (False,))
