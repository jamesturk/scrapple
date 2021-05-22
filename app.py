import csv
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/staff")
def staff():
    # thanks to http://www.figmentfly.com/bb/badguys3.html for names
    with open("data/employees.csv") as f:
        employees = list(csv.DictReader(f))

    return render_template("staff.html", employees=employees)
