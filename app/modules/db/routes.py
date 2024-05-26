from flask import render_template, request
from . import db

@db.route("/preview", methods=['GET'])
def preview():
    dbArray =  [
        {
            'id' : 1,
            'name': 'db1', 

        },
        {
            'id' : 2,
            'name': 'db2', 

        }
    ]
    return render_template('manage.html', dbs=dbArray)
