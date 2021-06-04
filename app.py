import csv
import math
from flask import Flask, render_template, abort, request

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
    page = int(request.args.get("page", 1))
    per_page = 10
    total_items = len(employees())
    max_page = math.ceil(total_items / per_page)
    print(max_page)
    if page < 1 or page > max_page:
        abort(404)
    page_employees = list(employees().values())[(page - 1) * per_page : page * per_page]
    return render_template(
        "staff.html",
        employees=page_employees,
        page=page,
        prev_page=page - 1,
        next_page=page + 1 if page < max_page else None,
    )


@app.route("/staff/<id_>")
def staff_detail(id_):
    if employee := employees().get(id_):
        return render_template("staff_detail.html", employee=employee)
    else:
        abort(404)
