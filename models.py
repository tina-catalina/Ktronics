from typing import Optional

from sqlalchemy.ext.declarative import declarative_base

from app.utils.settings import current_engine, get_session, engine_generator

Base = declarative_base()

def init_db(db_name: Optional[str] = None):
    from app.models.sys import SysUsers
    engine = current_engine() if not db_name else engine_generator[db_name]
    Session = get_session(engine)
    with Session() as session:
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        session.rollback()