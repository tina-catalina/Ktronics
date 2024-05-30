from app.utils.settings import get_session, current_engine
def create(data: dict, Model: object) -> any:
    Model = Model(**data)
    engine = current_engine()
    Session = get_session(engine)
    with Session() as session:
        try:
            session.add(Model)
            session.commit()
            return print(f"Created record for model: {Model}")
        except Exception as e: 
            session.rollback()
            raise e
