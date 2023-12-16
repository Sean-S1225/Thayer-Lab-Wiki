import os
from flask import Flask, render_template
from sys import path
path.append("./flaskr")
import GetUploadedContent
import FormatDocumentation

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/')
    @app.route('/home')
    def hello():
        return render_template("home.html")
    
    @app.route('/analyses')
    def analyses():
        return render_template("analyses.html")
    
    @app.route('/RMSD')
    def RMSD():
        return render_template("RMSD.html")

    @app.route('/RMSF')
    def RMSF():
        return render_template("RMSF.html")

    @app.route('/clustering')
    def Clustering():
        return render_template("clustering.html")
    
    @app.route('/papers')
    def RecentPublications():
        return render_template("papers.html")
    
    @app.route("/Intro")
    def Intro():
        return render_template("Intro.html")
    
    @app.route("/Theory")
    def Theory():
        return render_template("Theory.html")
    
    @app.route("/tleap")
    def Tleap():
        return render_template("tleap.html")
    
    @app.route("/emin")
    def Emin():
        return render_template("emin.html")
    
    @app.route("/heating")
    def Heating():
        return render_template("heating.html")
    
    @app.route("/equil")
    def Equil():
        return render_template("equil.html")
    
    @app.route("/neutral_dynamics")
    def NeutralDynamics():
        return render_template("neutral_dynamics.html")
    
    @app.route("/hbond")
    def HydrogenBonding():
        return render_template("hbond.html")
    
    @app.route("/SecStruct")
    def SecondaryStructure():
        return render_template("SecStruct.html")
    
    @app.route("/Ramachandran")
    def Ramachandran():
        return render_template("Ramachandran.html")
    
    @app.route("/MDSectors")
    def MDSectors():
        return render_template("MDSectors.html")
    
    @app.route("/electrostatics")
    def Electrostatics():
        return render_template("electrostatics.html")

    def GetCookbookPosts():
        posts = GetUploadedContent.GetValidJSONFiles(
            path="flaskr/Scripts_Templates",
            jsonName="Script.json",
            requiredFields=["Uploader_Name", "Created", "Last_Updated", "Program", "Name", "File_Name", "Description"],
            verify={
                "Created": GetUploadedContent.CheckDate,
                "Last_Updated": GetUploadedContent.CheckDate,
                "File_Name": lambda scriptName: os.path.isfile(os.path.join("flaskr/Scripts_Templates", scriptName))
            }
        )

        for index, post in enumerate(posts):
            post |= {"ID": index}

        return posts

    @app.route("/Cookbook")
    def Cookbook():
        return render_template("Cookbook.html", posts=GetCookbookPosts())
    
    @app.route("/post/<int:id>")
    def Recipe(id):

        recipes = GetCookbookPosts()
        recipe = next((r for r in recipes if r['ID'] == id), None)

        if recipe:
            temp = None
            with open("flaskr/Scripts_Templates/" + recipe["File_Name"], "r") as file:
                temp = file.readlines()
            recipe |= {"Script": temp}

        return render_template("recipe.html", post=recipe)

    def GetDocumentation():
        posts = GetUploadedContent.GetValidJSONFiles(
            path="flaskr/Documentation",
            jsonName="Documentation.json",
            requiredFields=["Uploader_Name", "Last_Updated", "Title", "File_Name", "Description"],
            verify={
                "Last_Updated": GetUploadedContent.CheckDate,
                "File_Name": lambda scriptName: os.path.isfile(os.path.join("flaskr/Documentation", scriptName))
            }
        )

        for post in posts:
            temp = None
            with open(os.path.join("flaskr/Documentation", post["File_Name"]), "r") as file: 
                temp = file.readlines()
            post |= {"Text": FormatDocumentation.FormatDocumentation(temp)}

        return posts

    @app.route("/Documentation")
    def Documentation():
        return render_template("Documentation.html", posts=GetDocumentation())

    return app