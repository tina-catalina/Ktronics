from typing import Optional

from app.utils.settings import get_session, current_engine


#Creates a new record in the database with the given model and also can be specified a session (used in create)
def create(data: dict, Model: object, session: Optional[object] = None) -> any:
    Model = Model(**data)
    engine = current_engine()
    Session = get_session(engine) if not session else session
    with Session() as session:
        try:
            session.add(Model)
            session.commit()
            return print(f"Created record for model: {Model}")
        except Exception as e: 
            session.rollback()
            raise e
