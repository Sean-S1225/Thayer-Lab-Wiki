import os
import json
from sys import path
path.append("../")
import unit_test

def GetScriptsTemplates(dir):
    scripts = []
    for x in os.listdir("./Scripts_Templates"):
        if os.path.isdir(os.path.join(dir, x)):
            scripts.append(os.path.join(dir, x))

    return scripts

def GetJSON(path):
    jsonData = None
    if os.path.isdir(path):
        path = os.path.join(path, "Script.json")
    with open(path, "r") as f:
        jsonData = json.load(f)

    return jsonData

def CheckDate(date):
    date = date.split(" ")
    if not len(date) == 3:
        return False
    
    months = ["January", "February", "March", "April", "May", "June", "July",
              "August", "September", "October", "November", "December"]
    
    return date[0] in months and str.isdigit(date[1]) and int(date[1]) <= 31 and len(str(date[2])) == 4

def CheckEverythingsThere(jsonDict):
    fields = ["Uploader Name", "Created", "Last Updated", "Program", "Name", "File Name", "Description"]
    for field in fields:
        if not field in jsonDict:
            return False
        
    if CheckDate(jsonDict["Created"]) == False or CheckDate(jsonDict["Last Updated"]) == False:
        return False
        
    return True

def GetValidScripts(dir="./Scripts_Templates"):
    files = GetScriptsTemplates(dir)
    data = []

    for file in files:
        temp = GetJSON(file)
        if CheckEverythingsThere(temp):
            data.append(temp)

    return data

if __name__ == "__main__":

    unit_test.UnitTest(CheckDate, ("October 31 2023",), (True,))
    unit_test.UnitTest(CheckDate, ("January 1 1990",), (True,))
    unit_test.UnitTest(CheckDate, ("January -1 1990",), (False,))
    unit_test.UnitTest(CheckDate, ("March 16.5 1990",), (False,))

    def TestHelper(file):
        return CheckEverythingsThere(GetJSON(file))

    unit_test.UnitTest(TestHelper, ("../tests/Scripts_Templates/Missing1.json",), (False,))
    unit_test.UnitTest(TestHelper, ("../tests/Scripts_Templates/Missing2.json",), (False,))
    unit_test.UnitTest(TestHelper, ("../tests/Scripts_Templates/WrongDate.json",), (False,))
    unit_test.UnitTest(TestHelper, ("../tests/Scripts_Templates/Extra.json",), (True,))
    unit_test.UnitTest(TestHelper, ("../tests/Scripts_Templates/Correct.json",), (True,))