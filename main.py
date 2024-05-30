from flask import render_template, redirect
from app import create_app

app = create_app()

# Here creates the .db_list.json file if it doesn't exist

with open(".db_list.json", "a") as f:
    f.close()

#TODO: Some validation to assure that for signup there's has to be a DB

@app.route("/")
def landing():
    return redirect("/home")

@app.route("/home")
def home():
    return render_template("index.html")
