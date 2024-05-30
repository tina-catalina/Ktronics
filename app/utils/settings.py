import os
import json
from os.path import basename
from typing import Optional

from dotenv import load_dotenv
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

import bcrypt

dotenv_path = basename(".env")
salt = bcrypt.gensalt()

load_dotenv(dotenv_path)

def get_env_variable(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the {} environment variable".format(var_name)
        raise EnvironmentError(error_msg)
    
def check_dbs(db_name: Optional[dict] = "", active_db: Optional[bool] = False):
    try:
        with open(".db_list.json", "r+") as f:
            dbs = json.load(f)
        
        if db_name:
            return dict(list(filter(lambda x: x['name'] == db_name, dbs["dbs"])))
        if active_db:
            return dict(list(filter(lambda x: x['is_active'] == True, dbs["dbs"])))
        return dbs
    except Exception as e:
        print(e)

def encrypt_password(password: str) -> str:
    return bcrypt.hashpw(bytes(password, 'utf-8'), salt)

def check_admin_password(password: str) -> bool:
    admin_password = check_dbs(active_db=True)["admin_password"]
    is_valid = bcrypt.checkpw(bytes(password, 'utf-8'), bytes(admin_password, 'utf-8'))
    if is_valid:
        return is_valid
    else:
        return False

def default_engine_generator():
    engine = create_engine(f"{get_env_variable('DB_TYPE')}://{get_env_variable('DB_USER')}:{get_env_variable('DB_PASSWORD')}@{get_env_variable('DB_HOST')}:{get_env_variable('DB_PORT')}/{get_env_variable('DB_TYPE_DEFAULT_DB')}")
    engine.raw_connection().set_isolation_level(
        ISOLATION_LEVEL_AUTOCOMMIT
    )
    return engine

def engine_generator():
    dbs = check_dbs()["dbs"]
    engines = {}
    for db in dbs:
        engines[db["name"]] = create_engine(f"{get_env_variable('DB_TYPE')}://{get_env_variable('DB_USER')}:{get_env_variable('DB_PASSWORD')}@{get_env_variable('DB_HOST')}:{get_env_variable('DB_PORT')}/{db["name"]}")
    return engines

def current_engine() -> Engine:
    actual_db = check_dbs(active_db=True)["name"]
    print(actual_db)
    engines = engine_generator()
    return engines[actual_db]

def get_session(engine):
    Session = sessionmaker(bind=engine)
    return Session

def add_db(vals: list) -> None:
    dbs = check_dbs()
    try:
        dbs['dbs'].append({
            'name': vals[0],
            'admin_password': str(vals[1]),
            'is_active': True if not dbs['dbs'] else False
        })
        json.dump(dbs, open('.db_list.json', 'w'), indent=4)
    except Exception as e:
        print(e)

def del_db(db_name: str) -> None:
    with open('.db_list.json', 'r+') as f:
        dbs = json.load(f)
        dbs['dbs'] = list(filter(lambda x: x['name'] != db_name, dbs['dbs']))
        json.dump(dbs, f, indent=4)

def upd_db(db_name: str) -> None:
    db_list: list[dict] = check_dbs()
    try:
        for db in db_list['dbs']:
            if db["name"] == db_name:
                db["is_active"] = True
            else:
                db["is_active"] = False
        json.dump(db_list, open(".db_list.json", "w"), indent=4)
    except Exception as e:
        print(e)