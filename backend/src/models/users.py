from sqlalchemy import Column, Integer, String

from db.postgres import Base


# User example - need to be refactored
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
