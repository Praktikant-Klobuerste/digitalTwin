from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, URL
import json
from datetime import datetime
import uuid




app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
title = "Modelfabrik 🎈"
sammlung = []

class TurmForm(FlaskForm):
    deckel = SelectField("Welche Farbe soll der Deckel haben?", choices=[("blau","🔵"),("rot","🔴"), ("schwarz","⚫")])
    mitte = SelectField("Welche Farbe soll die Mitte Haben?", choices=[("rot","🔴"), ("schwarz","⚫")])
    boden = SelectField("Welche Farbe soll der Boden haben?", choices=[("blau","🔵"),("rot","🔴")])
    submit = SubmitField("Bestellen")



class TurmSammlung():
    def __init__(self, *türme) -> None:
        self.türme = türme

    def __str__(self):
        return f"Eine Sammlung von {len(self.türme)}Türmen"


class Turm():
    def __init__(self, deckel, mitte, boden) -> None:
        self.deckel = deckel
        self.mitte = mitte
        self.boden = boden
        self.description = self.__repr__()

    def __repr__(self):
        return f"<Turm({self.deckel}, {self.mitte}, {self.boden})>"


def save_turm_json(turm):
    new_data = {
        "Turm": {
            "deckel" : turm.deckel,
            "mitte" : turm.mitte,
            "boden" : turm.boden,
            "beschreibung" : turm.description
        },
        "Zeit": {
            "tag" : datetime.now().strftime("%A"),
            "datum": datetime.now().strftime("%d.%m.%Y"),
            "komplett": datetime.now().strftime("%c"),
            "timestamp" : datetime.now().strftime("%X")
        },
        "uuid": str(uuid.uuid1())
    }


    try:
        with open("./bestellung.json", "r") as file:
            data = json.load(file)
        
    except FileNotFoundError:
        with open("./bestellung.json", "w") as file:
            file.write(json.dumps([new_data], indent=4))

    except ValueError:
        with open("./bestellung.json", "w") as file:
            file.write(json.dumps([new_data], indent=4))

    else:
        with open("./bestellung.json", "w") as file:
            data.append(new_data)
            file.write(json.dumps(data, indent=4))
            return data


def get_türme_json():
    try:
        with open("./bestellung.json", "r") as file:
            return json.load(file)

    except FileNotFoundError:
            return

    except ValueError:
            return


def find(lst, key, value):
    for i, dic in enumerate(lst):
        if dic[key] == value:
            return i
    return -1

@app.route("/")
def index():
    return render_template("index.html", title= title)



@app.route("/bauen", methods = ["GET", "POST"])
def bauen():
    form = TurmForm()
    türme = get_türme_json()
    # if request.method == "POST":
    try: 
        türme_anzahl = len(türme)
    except TypeError:
        türme_anzahl = None

    if form.validate_on_submit():
        turm = Turm(form.deckel.data, form.mitte.data, form.boden.data)
        print(turm)
        save_turm_json(turm)
        sammlung.append(turm)

        # print(sammlung)

        return redirect(url_for("bauen"))
    return render_template("bauen.html", title= "Bauen", form = form, türme = türme, türme_anzahl=türme_anzahl)


@app.route("/delete")
def delete_orderlist():
    turm_id = request.args.get("id")
    print(turm_id)
    if turm_id == "all":
        with open("./bestellung.json", "w") as file:
            file.write("[]")

    else:
        with open("./bestellung.json", "r") as file:
            data = json.load(file)
        turm_index = find(data, "uuid", turm_id)
        data.pop(turm_index)

        with open("./bestellung.json", "w") as file:
            file.write(json.dumps(data, indent=4))

    return redirect(url_for('bauen'))


@app.route("/csv")
def create_csv():
    with open("./bestellung.json", "r") as file:
        türme = json.load(file)

    with open("./bestellung.csv", "w") as file:
        file.write("Modul1;Modul2;Modul3\n")

        for turm in türme:
            turm = turm["Turm"]

            if turm["boden"] == "blau":
                file.write("1;")
            else:
                file.write("2;")

            if turm["mitte"] == "rot":
                file.write("1;")
            else:
                file.write("2;")
            
            if turm["deckel"] == "schwarz":
                file.write("1\n")
            elif turm["deckel"] == "blau":
                file.write("2\n")
            else:
                file.write("3\n")

    with open("./bestellung.json", "w") as file:
            file.write("[]")


            

    return redirect(url_for('bauen'))








if __name__=='__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)