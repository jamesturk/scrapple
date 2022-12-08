import json
import math
from . import app
from flask import render_template, abort, request

_parks = {}


def parks():
    global _parks
    if not _parks:
        with open("data/parks.json") as f:
            _parks = {int(p["id"]): p for p in json.load(f)}
    return _parks


@app.route("/parks")
def park_list():
    page = int(request.args.get("page", 1))
    per_page = 10
    total_items = len(parks())
    max_page = math.ceil(total_items / per_page)
    if page < 1 or page > max_page:
        abort(404)
    page_parks = list(parks().values())[(page - 1) * per_page : page * per_page]
    return render_template(
        "parks.html",
        parks=page_parks,
        page=page,
        prev_page=page - 1,
        next_page=page + 1 if page < max_page else None,
    )


@app.route("/parks/<id_>")
def park_detail(id_):
    if park := parks().get(int(id_)):
        return render_template("park_detail.html", park=park)
    else:
        abort(404)
