import csv
from flask import Flask, render_template

app = Flask(__name__)

_employees = {}


def employees():
    # thanks to http://www.figmentfly.com/bb/badguys3.html for names
    global _employees
    if not _employees:
        with open("data/employees.csv") as f:
            _employees = {e["id"]: e for e in csv.DictReader(f)}
    return _employees


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/staff")
def staff():
    return render_template("staff.html", employees=employees().values())


@app.route("/staff/<id_>")
def staff_detail(id_):
    if employee := employees().get(id_):
        return render_template("staff_detail.html", employee=employee)
    else:
        raise 404
