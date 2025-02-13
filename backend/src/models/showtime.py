from sqlalchemy import Column, Integer, Numeric, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from db.postgres import Base


class Showtime(Base):
    __tablename__ = "showtimes"

    id = Column(Integer, primary_key=True, index=True)
    film_id = Column(Integer, ForeignKey("films.id"))
    hall_id = Column(Integer, ForeignKey("halls.id"))
    datetime = Column(DateTime, nullable=False)
    available_tickets = Column(Integer, nullable=False)
    total_tickets = Column(Integer, nullable=False)

    film = relationship("Film", back_populates="showtimes")
    hall = relationship("Hall", back_populates="showtimes")
    tickets = relationship("Ticket", back_populates="showtime")


class Hall(Base):
    __tablename__ = "halls"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)  # Example: "IMAX Hall 1"
    capacity = Column(Integer, nullable=False)
    hall_type = Column(String, nullable=False)  # Example: "IMAX", "3D", "Standard"

    showtimes = relationship("Showtime", back_populates="hall")


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    showtime_id = Column(Integer, ForeignKey("showtimes.id"))
    seat_number = Column(String, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    is_booked = Column(Boolean, default=False)

    showtime = relationship("Showtime", back_populates="tickets")
