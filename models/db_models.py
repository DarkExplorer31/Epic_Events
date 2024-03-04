"""Define models for DataBase"""

import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, Enum, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship

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
    password = Column(String, nullable=False)
    creation_date = Column(Date, default=datetime.now, nullable=False)
    first_using_password = Column(Boolean, default=True)

    contracts = relationship("Contract", back_populates="user")
    support_events = relationship("Event", back_populates="support")

    def __str__(self):
        return self.email


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    complete_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone_number = Column(String, unique=True, nullable=False)
    company_name = Column(String, nullable=False)
    creation_date = Column(Date, default=datetime.now, nullable=False)
    updating_date = Column(Date, default=datetime.now, nullable=False)

    contracts = relationship("Contract", back_populates="client")

    def __str__(self):
        representation = (
            f"{self.company_name}:"
            + "\ncontact: "
            + f"{self.complete_name},"
            + "\nemail du contact: "
            + f"{self.email},"
            + "\ntéléphone: "
            + f"{self.phone_number},"
            + "\ncréer le: "
            + f"{self.creation_date}"
            + "\n"
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
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    total_cost = Column(Float, nullable=False)
    balance = Column(Float, nullable=False)
    creation_date = Column(Date, default=datetime.now, nullable=False)
    status = Column(Enum(StatusEnum), nullable=False)

    user = relationship("User", back_populates="contracts")
    client = relationship("Client", back_populates="contracts")
    events = relationship("Event", back_populates="contract")

    def __str__(self):
        client_name = self.client.complete_name
        username = self.user.complete_name
        return (
            f"Id du contrat: {self.id}, client: {client_name},"
            + "\n"
            + f" commercial: {username}, coût total: {self.total_cost},"
            + f" reste à régler: {self.balance}, date de création: "
            + f" {self.creation_date}, status: {self.status}"
            + "\n"
        )


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    contract_id = Column(Integer, ForeignKey("contracts.id"), nullable=False)
    support_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    starting_event_date = Column(Date, nullable=False)
    ending_envent_date = Column(Date, nullable=False)
    location = Column(String, nullable=False)
    attendees = Column(Integer)
    notes = Column(String)

    contract = relationship("Contract", back_populates="events")
    support = relationship("User", back_populates="support_events")

    def __str__(self):
        return f"L'évènement {self.id}: {self.starting_event_date} à {self.ending_envent_date}, Localisation: {self.location}"
