import os
import json
from sys import path
path.append("../")
import unit_test

def GetUserUploadedScriptTemplateNames(dir: str) -> list[str]:
    """Gets the .json files corresponding to user-uploaded scripts. Each .json file should be named "Script.json",
    and should be located in a folder corresponding to the script.

    Args:
        dir: The directory to where scripts and templates live

    Returns:
        A list of the directories in the directory
    """
    scripts = []
    for x in os.listdir(dir):
        if os.path.isdir(os.path.join(dir, x)):
            scripts.append(os.path.join(dir, x))

    return scripts

def GetJSONData(path: str) -> dict:
    """Given the path to a .json file, returns the data contained in that file.

    Args:
        path: The path to the .json file

    Returns:
        The data in the .json file as a dictionary
    """
    jsonData = None
    with open(os.path.join(path, "Script.json"), "r") as f:
        jsonData = json.load(f)

    return jsonData

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

def CheckEverythingsThere(jsonDict: dict) -> bool:
    """Ensures that in the data contained in a json file, all the parameters that should be there are:
    * Uploader Name [string]
    * Created [date (string)]
    * Last Updated [date (string)]
    * Program [string]
    * Name [string]
    * File Name [string]
    * Description [string]

    Args:
        jsonDict: The data obtained from the .json file

    Returns:
        True if all of the necessary data is there, False otherwise.
    """
    fields = ["Uploader Name", "Created", "Last Updated", "Program", "Name", "File Name", "Description"]
    for field in fields:
        if not field in jsonDict:
            return False
        
    if CheckDate(jsonDict["Created"]) == False or CheckDate(jsonDict["Last Updated"]) == False:
        return False
        
    return True

def GetJSONDataFromDirectory(dir: str = "./Scripts_Templates") -> list[str]:
    """From the passed in directory, returns the json data contained in the files

    Args:
        dir (optional): The directory to read from. Defaults to "./Scripts_Templates".

    Returns:
        Data contained in the files
    """
    files = GetUserUploadedScriptTemplateNames(dir)
    data = []

    for file in files:
        temp = GetJSONData(file)
        if CheckEverythingsThere(temp):
            data.append(temp)

    return data

if __name__ == "__main__":

    unit_test.UnitTest(CheckDate, ("October 31 2023",), (True,))
    unit_test.UnitTest(CheckDate, ("January 1 1990",), (True,))
    unit_test.UnitTest(CheckDate, ("January -1 1990",), (False,))
    unit_test.UnitTest(CheckDate, ("March 16.5 1990",), (False,))

    def TestHelper(file):
        return CheckEverythingsThere(GetJSONData(file))

    unit_test.UnitTest(TestHelper, ("../tests/Scripts_Templates/Missing1.json",), (False,))
    unit_test.UnitTest(TestHelper, ("../tests/Scripts_Templates/Missing2.json",), (False,))
    unit_test.UnitTest(TestHelper, ("../tests/Scripts_Templates/WrongDate.json",), (False,))
    unit_test.UnitTest(TestHelper, ("../tests/Scripts_Templates/Extra.json",), (True,))
    unit_test.UnitTest(TestHelper, ("../tests/Scripts_Templates/Correct.json",), (True,))

    unit_test.UnitTest(GetJSONDataFromDirectory, ("../tests/Scripts_Templates/",), (
        [{'Uploader Name': 'Sean', 'Created': 'October 18 2023', 'Last Updated': 'October 19 2023',
          'Program': 'Python', 'Name': 'Dihedral RMSD (Numba)', 'File Name': './DihedralRMSDNumba.py',
          'Description': "Calculates Root-Mean-Squared Deviation (RMSD) of a protein's dihedral angles", 'New': 'nothing!'}, 
         {'Uploader Name': 'Sean', 'Created': 'October 18 2023', 'Last Updated': 'October 19 2023',
          'Program': 'Python', 'Name': 'Dihedral RMSD (Numba)', 'File Name': './DihedralRMSDNumba.py',
          'Description': "Calculates Root-Mean-Squared Deviation (RMSD) of a protein's dihedral angles"}],))