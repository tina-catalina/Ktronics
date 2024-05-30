from flask import render_template, redirect
from app import create_app

app = create_app()

# TODO: Validate if there's no DB in the .db_list file and redirect to create
# TODO: Create .db_list.json on start

@app.route("/")
def landing():
    return redirect("/home")

@app.route("/home")
def home():
    return render_template("index.html")
