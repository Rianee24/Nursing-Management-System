from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.exc import NoResultFound
from . import Base

class Manager(Base):
    __tablename__ = "managers"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    phone_number = Column(String)
    department = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    nurses = relationship("Nurse", back_populates="manager", cascade="all, delete-orphan")

    @classmethod
    def create(cls, session, name, email, phone_number=None, department=None):
        if not name.strip():
            raise ValueError("Manager name cannot be empty")
        if "@" not in email or "." not in email:
            raise ValueError("Invalid email")
        m = cls(name=name.strip(), email=email.strip(), phone_number=phone_number, department=department)
        session.add(m)
        session.commit()
        session.refresh(m)
        return m

    @classmethod
    def get_all(cls, session):
        return session.query(cls).order_by(cls.id).all()

    @classmethod
    def find_by_id(cls, session, id_):
        return session.get(cls, id_)

    @classmethod
    def find_by_attr(cls, session, attr, value):
        q = {attr: value}
        return session.query(cls).filter_by(**q).all()

    @classmethod
    def delete(cls, session, id_):
        obj = cls.find_by_id(session, id_)
        if not obj:
            raise NoResultFound(f"Manager id {id_} not found")
        session.delete(obj)
        session.commit()
        return True


class Nurse(Base):
    __tablename__ = "nurses"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    specialization = Column(String)
    shift = Column(String)
    manager_id = Column(Integer, ForeignKey("managers.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    manager = relationship("Manager", back_populates="nurses")
    elderly = relationship("Elderly", back_populates="nurse", cascade="all, delete-orphan")

    @classmethod
    def create(cls, session, name, specialization=None, shift=None, manager_id=None):
        if not name.strip():
            raise ValueError("Nurse name cannot be empty")
        n = cls(name=name.strip(), specialization=specialization, shift=shift, manager_id=manager_id)
        session.add(n)
        session.commit()
        session.refresh(n)
        return n

    @classmethod
    def get_all(cls, session):
        return session.query(cls).order_by(cls.id).all()

    @classmethod
    def find_by_id(cls, session, id_):
        return session.get(cls, id_)

    @classmethod
    def find_by_attr(cls, session, attr, value):
        q = {attr: value}
        return session.query(cls).filter_by(**q).all()

    @classmethod
    def delete(cls, session, id_):
        obj = cls.find_by_id(session, id_)
        if not obj:
            raise NoResultFound(f"Nurse id {id_} not found")
        session.delete(obj)
        session.commit()
        return True


class Elderly(Base):
    __tablename__ = "elderly"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer)
    health_condition = Column(String)
    nurse_id = Column(Integer, ForeignKey("nurses.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    nurse = relationship("Nurse", back_populates="elderly")

    @classmethod
    def create(cls, session, name, age=None, health_condition=None, nurse_id=None):
        if not name.strip():
            raise ValueError("Elderly name cannot be empty")
        if age is not None and (age < 0 or age > 130):
            raise ValueError("Age must be between 0 and 130")
        e = cls(name=name.strip(), age=age, health_condition=health_condition, nurse_id=nurse_id)
        session.add(e)
        session.commit()
        session.refresh(e)
        return e

    @classmethod
    def get_all(cls, session):
        return session.query(cls).order_by(cls.id).all()

    @classmethod
    def find_by_id(cls, session, id_):
        return session.get(cls, id_)

    @classmethod
    def find_by_attr(cls, session, attr, value):
        q = {attr: value}
        return session.query(cls).filter_by(**q).all()

    @classmethod
    def delete(cls, session, id_):
        obj = cls.find_by_id(session, id_)
        if not obj:
            raise NoResultFound(f"Elderly id {id_} not found")
        session.delete(obj)
        session.commit()
        return True
