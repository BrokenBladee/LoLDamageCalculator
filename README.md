# LoLDamageCalculator

Two Folders, one Database and one Python file


**'manage.py'** generated file by Django framework.

**'LoLDamageCalculator'** contains framework generated python file, like urls and settings, I made just a few of changes to add one URL.

**'db.sqlite3'** refers to the database.

**'dmgcalc'** contains the whole app, frontend and backend.

### dmgcalc content:

**'migrations'** folder contains .py files that were automatically created by the framework when migrating the sqlite databases from the
**'models.py'** file.

**'templates'** contains my index.html, which has all the CSS and JavaScript too.

**'admin.py' & 'apps.py' & 'tests.py'&** are all generated files by Django that I haven't touched

**urls.py** is a small file that conatins the url.

**'views.py' & 'models.py'** are my main two files. The models.py file contains all my tables for my sqlite3 database. The views.py file renders the index.html file and all the templates from my database, that I can use in my index.html to display the content or get user input in my database. It also contains all the calculation.

## How to locally open and use the website with VSCode:
Clone the git repository and open with VSCode, either install Python or install the Python extension, if you want to check the database install the sqlite extension and then rightclick on db.sqlite3 and choose Open Database which will open it in the left corner, where you can choose the tables. Now create a virtual envirenmont using following commands in the console:
```
python3 -m venv .venv
```
```
source .venv/bin/activate
```
Then install pip and Django:
```
python -m pip install --upgrade pip
```
```
python -m pip install django
```
Now you can run the app by typing:
```
python manage.py runserver
