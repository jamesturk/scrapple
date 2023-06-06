import csv
import math
from . import app
from flask import render_template, abort, request


_employees = {}


def employees():
    # thanks to http://www.figmentfly.com/bb/badguys3.html for names
    global _employees
    if not _employees:
        with open("data/employees.csv") as f:
            _employees = {e["id"]: e for e in csv.DictReader(f)}
    return _employees


@app.route("/awards")
def awards():
    award_data = [
        {
            "name": "Nobel Prize in Physics",
            "year": "1934",
            "for": "Discovery of the 8th Dimension",
            "to": "John Whorfin",
        },
        {
            "name": "Cousteau Society Award",
            "year": "1989",
            "for": "Uses of Cephalopod Intelligence",
            "to": "John Fish",
        },
        {
            "name": "Best Supporting Actor",
            "year": "1985",
            "for": "John Lithgow Biopic",
            "to": "John Whorfin",
        },
        {
            "name": "Nobel Prize in Physics",
            "year": "2986",
            "for": "Temporal Paradox Resolution",
            "to": "John O'Connor",
        },
        {
            "name": "Paralegal of the Year",
            "year": "1999",
            "for": "Paralegal Activity",
            "to": "John Two Horns",
        },
        {
            "name": "ACM Award",
            "year": "1986",
            "for": "Innovations in User Interface",
            "to": "John Ya Ya",
        },
        {
            "name": "2nd Place, Most Jars Category",
            "year": "1987",
            "for": "Jars",
            "to": "John Many Jars",
        },
        {
            "name": "Album of the Year",
            "year": "1997",
            "for": "Space Coyote",
            "to": "John Coyote",
        },
        {
            "name": "Most Creative Loophole",
            "year": "1985",
            "for": "Innovation in Interdimensional Tax Shelters",
            "to": "John Lee",
        },
    ]
    return render_template("awards.html", awards=award_data)


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
    # check style parameter
    style = request.args.get("style", "")
    if style == "new":
        template = "staff_detail_new.html"
    elif style == "experimental":
        template = "staff_detail_experimental.html"
    else:
        template = "staff_detail.html"

    if id_ == "404":
        abort(
            404,
            "This page intentionally left blank. (No really! This is an intentional error for demonstration purposes.)",
        )
    if employee := employees().get(id_):
        return render_template("staff_detail.html", employee=employee)
    else:
        abort(404)
