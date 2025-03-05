from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship

from db.postgres import Base


class Film(Base):
    __tablename__ = "films"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    genre = Column(String, nullable=False)
    duration = Column(Integer, nullable=False)  # In minutes
    age_restriction = Column(String, nullable=False)  # Example: "PG-13"
    imdb_rating = Column(Float, nullable=True)
    description = Column(String, nullable=True)
    poster_url = Column(String, nullable=True)  # Link to image
    showtimes = relationship("Showtime", back_populates="film")
