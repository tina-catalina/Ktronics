from typing import Optional

from flask import render_template, request, make_response, redirect
from sqlalchemy import text

from . import db
from app.utils.settings import (
    check_dbs, 
    engine_generator,
    default_engine_generator, 
    get_session, 
    add_db, 
    encrypt_password, 
    del_db, 
    upd_db
)
from app.models.sys import SysUsers
from app.utils.crud import create as create_model
from models import init_db


#TODO: Some kind of visual validation for select which password is currenttly being used, perhaps in the view
#First the DB preview search for the created DB, the list is in the .db_list file and returns the dbs as context
@db.route("/preview", methods=["GET", "POST"])
def preview():
    dbs = check_dbs()
    ctx = dbs if dbs else {}
    return render_template("manage.html", **ctx)


#This endpoint changes the active DB, getting the name of the clicked DB on the view and redirects to preview after that
@db.route("/preview/<db_name>", methods=["POST"])
def preview_change(db_name):
    upd_db(db_name)
    response = make_response(redirect("/db/preview"))
    return response


#Create gets form data, if there's a POST and data provided, creates the DB, if it's the first DB of the program
#It's going to set as active DB, it can be changed later and after that, create the first User (Admin)
@db.route("/create", methods=["GET", "POST"])
def create():
    data = request.form.to_dict(flat=True)

    if request.method == "POST" and data:
        response = make_response(redirect("/db/preview"))
        try:
            encrypted_password = encrypt_password(data["password"])
            create_db(encrypted_password, data["db_name"])
            model_data = {
                "name": data["admin_name"],
                "password": encrypted_password,
                "email": f"{data['admin_name']}",
                "is_admin": True
            }
            engine = engine_generator()[data["db_name"]]
            Session = get_session(engine)
            create_model(model_data, SysUsers, Session)
        except Exception as e:
            print(e)
        return response        
    else:
        return render_template("create.html")


# TODO: Validate password on delete
#Delete gets the name of the DB and redirects to preview after delete the clicked DB
@db.route("/delete/<name>", methods=["GET", "POST"])
def delete(name):
    response = make_response(redirect("/db/preview"))
    if request.method == "POST" and name:
        delete_db(name)
        return response
    else:
        return response


#Creates new transaction and with the Password and DB Name creates the first DB
def create_db(admin_password: str, db_name: Optional[str]):
    if db_name and admin_password:
        #Creating a new connection transaction in order to execute CREATE statement
        query: text = text(f"CREATE DATABASE {db_name};")
        try:
            engine = default_engine_generator()
            Session = get_session(engine)
            with Session() as session:
                session.execute(query)
                db: list = [db_name, admin_password, True]
                add_db(db)
                session.commit()
        except Exception as e:
            print(e)
        init_db(db_name)
    else: 
        return print("You have to provide a password and db name")


# TODO: Some bugs with delete, determine why sessions are not closing correctly in order to delete the DB, on refresh or reload it works as supposed
#Creates new transaction and deletes the given DB
def delete_db(db_name: Optional[str] = None) -> any:
    if db_name:
        query: text = text(f"DROP DATABASE {db_name};")
        engine = default_engine_generator()
        Session = get_session(engine)
        try:
            with Session() as session:
                session.execute(query)
                del_db(db_name)
                session.commit()
        except Exception as e:
            print(e)
    else: 
        return print("You have to provide a DB name")
