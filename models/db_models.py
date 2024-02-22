"""Define models for DataBase"""

import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, Enum, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy import event

from db import Base


class RoleEnum(enum.Enum):
    SALES = "Sales"
    MANAGER = "Manager"
    SUPPORT = "Support"

    def __str__(self):
        return self.value


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    role = Column(Enum(RoleEnum), nullable=False)
    complete_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone_number = Column(String, unique=True, nullable=False)
    password = Column(String)
    creation_date = Column(Date, default=datetime.now, nullable=False)
    first_using_password = Column(Boolean, default=True)

    contracts = relationship("Contract", back_populates="users")

    def __str__(self):
        return self.email


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    complete_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone_number = Column(String, unique=True, nullable=False)
    company_name = Column(String, nullable=False)
    creation_date = Column(Date, default=datetime.now, nullable=False)
    updating_date = Column(Date, default=datetime.now, nullable=False)

    contracts = relationship("Contract", back_populates="client")

    def __str__(self):
        representation = (
            f"{self.company_name}: contact:{self.complete_name},"
            + "\n"
            + f" email du contact:{self.email},  téléphone: "
            + "\n"
            + f"{self.phone_number}, créer le: {self.creation_date}"
        )
        return representation


class StatusEnum(enum.Enum):
    UNSIGNED = "Non signé"
    UNPAID = "Pas payer"
    PAID = "Payer"

    def __str__(self):
        return self.value


class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    client_id = Column(Integer, ForeignKey("clients.id"), unique=True, nullable=False)
    total_cost = Column(Float, nullable=False)
    balance = Column(Float, nullable=False)
    creation_date = Column(Date, default=datetime.now, nullable=False)
    status = Column(Enum(StatusEnum), nullable=False)

    users = relationship("User", back_populates="contracts")
    client = relationship("Client", back_populates="contracts")
    events = relationship("Event", back_populates="contract")


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    contract_id = Column(
        Integer, ForeignKey("contracts.id"), unique=True, nullable=False
    )
    starting_event_date = Column(Date, nullable=False)
    ending_envent_date = Column(Date, nullable=False)
    support_contact_name = Column(String)
    localisation = Column(String, nullable=False)
    attendees = Column(Integer)
    notes = Column(String)

    contract = relationship("Contract", back_populates="events")
