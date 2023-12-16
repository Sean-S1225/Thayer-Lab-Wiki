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

def CheckFile(file: str, prefix) -> bool:
    """Ensures the file is an actual file, and the correct one

    Args:
        file: The string to check

    Returns:
        True if the string is valid, False otherwise
    """

    toReturn = False
    try:
        toReturn = os.path.isfile(os.path.join(prefix, file))
    except NotADirectoryError:
        return False
    
    return toReturn

def CheckEverythingsThere(jsonDict: dict, prefix = "flaskr/Scripts_Templates") -> bool:
    """Ensures that in the data contained in a json file, all the parameters that should be there are:
    * Uploader_Name [string]
    * Created [date (string)]
    * Last_Updated [date (string)]
    * Program [string]
    * Name [string]
    * File_Name [string]
    * Description [string]

    Args:
        jsonDict: The data obtained from the .json file

    Returns:
        True if all of the necessary data is there, False otherwise.
    """
    fields = ["Uploader_Name", "Created", "Last_Updated", "Program", "Name", "File_Name", "Description"]
    for field in fields:
        if not field in jsonDict:
            return False
    
    if CheckDate(jsonDict["Created"]) == False or CheckDate(jsonDict["Last_Updated"]) == False:
        return False
    
    if CheckFile(jsonDict["File_Name"], prefix) == False:
        return False
    
    return True

def GetJSONDataFromDirectory(dir: str = "flaskr/Scripts_Templates") -> list[str]:
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
            temp |= {"ID": len(data)}
            data.append(temp)

    return data

if __name__ == "__main__":

    unit_test.UnitTest(CheckDate, ("October 31 2023",), (True,))
    unit_test.UnitTest(CheckDate, ("January 1 1990",), (True,))
    unit_test.UnitTest(CheckDate, ("January -1 1990",), (False,))
    unit_test.UnitTest(CheckDate, ("March 16.5 1990",), (False,))


    unit_test.UnitTest(CheckFile, ("Dihedral RMSD/DihedralRMSDNumba.py", "./Scripts_Templates/"), (True,))
    unit_test.UnitTest(CheckFile, ("Dihedral RMSD/DihedralRMSDNumba.py", "./"), (False,))

    def TestHelper(file):
        return CheckEverythingsThere(GetJSONData(file), "../tests/Scripts_Templates/")

    unit_test.UnitTest(TestHelper, ("../tests/Scripts_Templates/Missing1",), (False,))
    unit_test.UnitTest(TestHelper, ("../tests/Scripts_Templates/Missing2",), (False,))
    unit_test.UnitTest(TestHelper, ("../tests/Scripts_Templates/WrongDate",), (False,))
    unit_test.UnitTest(TestHelper, ("../tests/Scripts_Templates/WrongDate2",), (False,))
    unit_test.UnitTest(TestHelper, ("../tests/Scripts_Templates/Extra",), (True,))
    unit_test.UnitTest(TestHelper, ("../tests/Scripts_Templates/Correct",), (True,))

    unit_test.UnitTest(GetJSONDataFromDirectory, ("../tests/Scripts_Templates/",), (
        [{'Uploader_Name': 'Sean', 'Created': 'October 18 2023', 'Last_Updated': 'October 19 2023',
          'Program': 'Python', 'Name': 'Dihedral RMSD (Numba)', 'File_Name': 'Correct/test.py',
          'Description': "Calculates Root-Mean-Squared Deviation (RMSD) of a protein's dihedral angles", "ID": 0}, 
         {'Uploader_Name': 'Sean', 'Created': 'October 18 2023', 'Last_Updated': 'October 19 2023',
          'Program': 'Python', 'Name': 'Dihedral RMSD (Numba)', 'File_Name': 'Extra/test.py',
          'Description': "Calculates Root-Mean-Squared Deviation (RMSD) of a protein's dihedral angles", 'New': 'nothing!', "ID": 1}],))