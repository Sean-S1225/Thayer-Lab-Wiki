"""

IMPORTANT: Most of this will likely need to be re-written, but it will serve as a very rough starting structure.

"""

from flask import Flask
import GetScriptsTemplates

app = Flask(__name__, instance_relative_config=True)

@app.route("/")
def HomePage():
    pass

@app.route("/GeneralInfo")
def GeneralInfo():
    pass

@app.route("/GeneralInfo/MDSimulations")
def MDSimulations():
    pass

@app.route("/GeneralInfo/Theory")
def Theory():
    pass

@app.route("/GeneralInfo/Setup")
def Setup():
    pass

@app.route("/GeneralInfo/TLEAP")
def TLEAP():
    pass

@app.route("/GeneralInfo/EMin")
def EMin():
    pass

@app.route("/GeneralInfo/Heat")
def Heat():
    pass

@app.route("/GeneralInfo/Equil")
def Equil():
    pass

@app.route("/GeneralInfo/MD")
def MD():
    pass

@app.route("/Analyses")
def Analyses():
    pass

@app.route("/Analyses/RMSD")
def RMSD():
    pass

@app.route("/Analyses/RMSF")
def RMSF():
    pass

@app.route("/Analyses/Clustering")
def Clustering():
    pass

@app.route("/Analyses/HBond")
def HBond():
    pass

@app.route("/Analyses/SecStruct")
def SecStruct():
    pass

@app.route("/Papers")
def Papers():
    pass

@app.route("/Misc")
def Misc():
    pass

@app.route("/Code")
def Code():
    data = GetScriptsTemplates.GetJSONDataFromDirectory()
    for d in data:
        #Generate page based on each script
        pass