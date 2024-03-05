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
        return (
            f"Role: {self.role}\n"
            + f"Nom complet: {self.complete_name}\n"
            + f"Email: {self.email}\n"
            + f"Numéro de téléphone: {self.phone_number}\n"
            + f"Date de création: {self.creation_date}\n"
        )


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
        return (
            f"Nom complet: {self.complete_name}\n"
            + f"Email: {self.email}\n"
            + f"Numéro de téléphone: {self.phone_number}\n"
            + f"Nom de l'entreprise: {self.company_name}\n"
            + f"Date de création: {self.creation_date}\n"
            + f"Date de mise à jour: {self.updating_date}\n\n"
        )


class StatusEnum(enum.Enum):
    UNSIGNED = "Non signé"
    UNPAID = "Pas payé"
    PAID = "Payé"

    def __str__(self):
        return self.value


class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    total_cost = Column(Float, nullable=False)
    balance = Column(Float)
    creation_date = Column(Date, default=datetime.now, nullable=False)
    status = Column(Enum(StatusEnum), nullable=False)

    user = relationship("User", back_populates="contracts")
    client = relationship("Client", back_populates="contracts")
    events = relationship("Event", back_populates="contract")

    def __str__(self):
        client_name = self.client.complete_name
        commercial = self.user.complete_name
        return (
            f"ID du contrat: {self.id}\n"
            + f"Client: {client_name}\n"
            + f"Commercial: {commercial}\n"
            + f"Coût total: {self.total_cost}\n"
            + f"Reste à régler: {self.balance}\n"
            + f"Date de création: {self.creation_date}\n"
            + f"Statut: {self.status}\n\n"
        )


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    contract_id = Column(Integer, ForeignKey("contracts.id"), nullable=False)
    support_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    starting_event_date = Column(Date, nullable=False)
    ending_event_date = Column(Date, nullable=False)
    location = Column(String, nullable=False)
    attendees = Column(Integer)
    notes = Column(String)

    contract = relationship("Contract", back_populates="events")
    support = relationship("User", back_populates="support_events")

    def __str__(self):
        support_name = self.support.complete_name if self.support else "Non affecté"
        return (
            f"ID de l'évènement: {self.id}\n"
            + f"Affecté à: {support_name}\n"
            + f"Date de début: {self.starting_event_date}\n"
            + f"Date de fin: {self.ending_event_date}\n"
            + f"Localisation: {self.location}\n"
            + f"Nombre de participants: {self.attendees}\n"
            + f"Notes: {self.notes}\n\n"
        )
