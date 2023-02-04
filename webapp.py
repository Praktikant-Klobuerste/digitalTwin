from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, URL
import json
from datetime import datetime




app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
title = "Modelfabrik 🎈"
sammlung = []

class TurmForm(FlaskForm):
    deckel = SelectField("Welche Farbe soll der Deckel haben?", choices=[("rot","🔴"), ("schwarz","⚫")])
    mitte = SelectField("Welche Farbe soll die Mitte Haben?", choices=[("blau","🔵"),("rot","🔴"), ("schwarz","⚫")])
    boden = SelectField("Welche Farbe soll der Boden haben?", choices=[("blau","🔵"),("rot","🔴")])
    submit = SubmitField("Submit")


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
        }
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





@app.route("/")
def index():
    return render_template("index.html", title= title)



@app.route("/bauen", methods = ["GET", "POST"])
def bauen():
    form = TurmForm()
    # if request.method == "POST":
    if form.validate_on_submit():
        turm = Turm(form.deckel.data, form.mitte.data, form.boden.data)
        print(turm)
        save_turm_json(turm)
        sammlung.append(turm)

        # print(sammlung)

        # return redirect(url_for("index"))
    return render_template("bauen.html", title= "Bauen", form = form)








if __name__=='__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)