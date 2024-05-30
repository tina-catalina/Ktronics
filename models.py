from typing import Optional

from sqlalchemy.ext.declarative import declarative_base

from app.utils.settings import get_session, engine_generator, current_engine

Base = declarative_base()


'''
    This function will be called every time a DB is created using it's name as arg, 
    it can work for resetting the DB due to drop_all with the same arg.
    If you dont pass any arg it'll just delete the current DB
'''
def init_db(db_name: Optional[str] = None) -> None:
    from app.models.sys import SysUsers
    engine = engine_generator()[db_name] if db_name else current_engine()
    Session = get_session(engine)
    with Session() as session:
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        session.rollback()
