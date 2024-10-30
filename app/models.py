from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Column
from typing import List
from datetime import date


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class = Base)

service_mechanics = db.Table(
    "service_mechanics",
    Base.metadata,
    Column("ticket_id", db.ForeignKey("service_tickets.id")),
    Column("mechanic_id", db.ForeignKey("mechanics.id"))
)

class Customer(Base):
    __tablename__ = 'customers'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(100), nullable = False)
    email: Mapped[str] = mapped_column(db.String(200), nullable= False, unique=True)
    phone: Mapped[str] = mapped_column(db.String(25))
    password: Mapped[str] = mapped_column(db.String(200), nullable=False)
    role: Mapped[str] = mapped_column(db.String(50), nullable=False)

    service_tickets: Mapped[List['ServiceTicket']] = db.relationship(back_populates = 'customer')


class ServiceTicket (Base):
    __tablename__ = 'service_tickets'

    id: Mapped[int] = mapped_column(primary_key=True)
    vin: Mapped[str] = mapped_column (db.String(100), nullable=False)
    service_date: Mapped[date] = mapped_column (nullable=False)
    service_desc: Mapped[str] = mapped_column (db.String(300))
    customer_id: Mapped[int] = mapped_column(db.ForeignKey('customers.id'))

    customer: Mapped['Customer'] = db.relationship(back_populates = 'service_tickets')
    mechanics: Mapped[List["Mechanic"]] = db.relationship(secondary = service_mechanics, back_populates='service_tickets')

class Mechanic (Base):
    __tablename__ = 'mechanics'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(100), nullable = False)
    email: Mapped[str] = mapped_column(db.String(200), nullable= False, unique=True)
    phone: Mapped[str] = mapped_column(db.String(25))
    salary: Mapped[float] = mapped_column()

    service_tickets: Mapped[List['ServiceTicket']] = db.relationship(secondary = service_mechanics, back_populates = 'mechanics')


