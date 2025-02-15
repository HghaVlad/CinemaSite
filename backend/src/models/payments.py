import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DATETIME, DECIMAL, Enum
from sqlalchemy.orm import relationship

from db.postgres import Base


class PaymentStatus(str, enum.Enum):
    SUCCESS = 1
    FAILED = 2
    NOT_ENOUGH_MONEY = 3
    ERROR = 4


class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DATETIME, default=datetime.utcnow)
    price = Column(DECIMAL(10, 2))

    ticket = relationship("Ticket", back_populates="bookings")


class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"))
    card_number = Column(String)
    card_holder = Column(String)
    cvv = Column(Integer)
    status = Column(Enum(PaymentStatus), default=PaymentStatus.FAILED)
    created_at = Column(DATETIME, default=datetime.utcnow)

    booking = relationship("Bookings", back_populates="payments")


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    ticket_id = Column(Integer, ForeignKey("tickets.id"))
    payment_id = Column(Integer, ForeignKey("payments.id"))
    created_at = Column(DATETIME, default=datetime.utcnow)

    ticket = relationship("Ticket", back_populates="orders")