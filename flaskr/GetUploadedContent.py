from collections import callable
import os

def GetDirectories(path: str) -> list[str]:
    """Gets all directories in the user-uploaded section. This is the first step,
    more logic will follow to verify the data contained"""
    pass

def GetJSONFiles(directories: list[str]) -> list[dict]:
    """Gets all .json files associated with user uploaded scripts"""
    pass

def CheckJSONFiles(jsonFiles: list[dict], requiredFields: list[str]) -> list[dict]:
    """Returns the .json dictionaries that have all of the required fields"""

def VerifyFields(jsonFiles: list[dict], verify: dict[str, callable[[str], bool]]) -> list[dict]:
    """Returns the .json dictionaries that pass some sort of verification on a specific field"""

