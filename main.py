from flask import Flask, render_template, abort, make_response, request, redirect, url_for

import data

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html",
                           departures=data.departures,
                           title=data.title,
                           subtitle=data.subtitle,
                           descripton=data.description,
                           tours=data.tours,
                           cookie=request.cookies.get("username"))


@app.route("/login/", methods=["GET", "POST"])
def login():
    if not request.cookies.get("username") and request.method == "POST":
        res = make_response("Seting a coockie")
        res.set_cookie("username", request.form.get(
            "name"), max_age=60 * 60 * 24 * 365 * 2)
        return res
    return render_template("login.html")


@app.route("/cookie/")
def cookie():
    if not request.cookies.get("username") or request.cookies.get("username") == "None":
        return redirect(url_for("login"))
    else:
        res = make_response(
            f"Value of cookie is {request.cookies.get('username')}")
        return res


@app.route("/departure/")
def departures():
    return render_template("index.html")


@app.route("/departures/<departure>/")
def departure(departure):
    tours = dict(
        filter(lambda tour: tour[1]["departure"] == departure, data.tours.items()))
    if tours:
        return render_template("departure.html",
                               departure=departure,
                               departures=data.departures,
                               title=data.title,
                               tours=tours)

    abort(404)


@app.route("/tour/")
def list_tour():
    return render_template("tour.html")


@app.route("/tours/<int:id>/")
def tours(id):
    return render_template("tour.html",
                           tour=data.tours[id],
                           title=data.title,
                           departures=data.departures)


@app.route("/agent/")
def agent():
    user_agent = request.headers.get("User-Agent")
    return f"<b>Your browser is {user_agent}</b>"


app.run(debug=True)
