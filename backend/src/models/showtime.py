from sqlalchemy import Column, Integer, Numeric, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from db.postgres import Base


class Showtime(Base):
    __tablename__ = "showtimes"

    id = Column(Integer, primary_key=True, index=True)
    film_id = Column(Integer, ForeignKey("films.id"))
    datetime = Column(DateTime, nullable=False)
    total_tickets = Column(Integer, nullable=False)
    rows = Column(Integer, nullable=False)
    places = Column(Integer, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)

    film = relationship("Film", back_populates="showtimes")
    tickets = relationship("Ticket", back_populates="showtime")


class Hall(Base):
    __tablename__ = "halls"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)  # Example: "IMAX Hall 1"
    capacity = Column(Integer, nullable=False)
    rows = Column(Integer, nullable=False) # Количество рядов
    places = Column(Integer, nullable=False) # Количество мест в ряду
    hall_type = Column(String, nullable=False)  # Example: "IMAX", "3D", "Standard"



class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    showtime_id = Column(Integer, ForeignKey("showtimes.id"))
    price = Column(Numeric(10, 2), nullable=False)
    row = Column(Integer, nullable=False)
    place = Column(Integer, nullable=False)

    showtime = relationship("Showtime", back_populates="tickets")
