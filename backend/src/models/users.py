from sqlalchemy import Column, Integer, String

from db.postgres import Base


# User example - need to be refactored
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    name = Column(String)
    surname = Column(String)
