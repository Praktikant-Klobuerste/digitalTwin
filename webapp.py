from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, URL




app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
title = "Modelfabrik 🎈"

class TurmForm(FlaskForm):
    mitte = SelectField("Welche Farbe soll die Mitte Haben?", choices=["🔵","🔴", "⚫"])
    deckel = SelectField("Welche Farbe soll der Deckel haben?", choices=["🔴", "⚫"])
    boden = SelectField("Welche Farbe soll der Boden haben?", choices=["🔵","🔴"])
    submit = SubmitField("Submit")



@app.route("/")
def index():
    return render_template("index.html", title= title)

@app.route("/bauen")
def bauen():
    form = TurmForm()
    if form.validate_on_submit():
        return redirect(url_for("index"))
    return render_template("bauen.html", title= "Bauen", form = form)








if __name__=='__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)