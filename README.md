# Thayer Lab Wiki

#Instructions:
Make sure you have the following packages installed via your favorite installer (pip, homebrew, etc):
* flask
* os
* sys
* collections
* re
* json
* beautifulsoup4
* requests

To run the project, `cd` into the ThayerLab directory, then run `python3 ThayerLabWebsite.py`.
If this doesn't work, try the command 
```flask --app flaskr run --debug```.
In either case, in the browser of your choice, open the link http://127.0.0.1:5000/. This will bring you to the home page of the website!

To run the tests, you can run
```
cd flaskr
python3 FormatDocumentation.py
python3 GetPapers.py
python3 GetUploadedContent.py
```

I want to design a wiki page for people in the Thayer Lab at Wesleyan University, both incoming students to the lab and seasoned students who need a refresher on certain topics. As is the case with all labs, our lab as a large amount of highly specific tools, processes, techniques, and strategies that we employ to do research. For an incoming student, this is like drinking from a firehose. I would like to help streamline the process and aid the new student as they learn about tools employed by the lab, while also providing a resource of code and troubleshooting techniques to the more experienced lab members.

In this website, I would like to provide:
* General introductory information (what molecular dynamic simulations are, how to set them up and run them)
* Common analyses (RMSD, RMSF, Clustering, etc)
* Miscellaneous pieces of accumulated knowledge (how to import specific packages, certain specific procedures, etc)
* Links to resources, previous papers, etc
* Template code for any and all of the above

I have already written a lot of code, some of it as already been added to this repository, but it is highly specialized to my needs, and is therefore in need of refactoring to serve the needs of others. The rest of the website will be designed from the ground up.

My intention is that this wiki will be for the members of the Thayer Lab. It will contain information about our research for the people who are doing our research. However, the processes, code, tools our lab develops are not proprietary; and anyone should be able to access it (though most likely only other researchers in the field will). The goal is for the barrier-to-entry in terms of knowledge to be as low as possible, so anyone who can browse a website should be able to use it :).

There are not many stakeholders of this project who are not direct users. The only non-user stakeholders are the people who may be treated with drugs designed in labs such as our lab. But that is very far off; we are in a sense the "first line" in drug development. 
