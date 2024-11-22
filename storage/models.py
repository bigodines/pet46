from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class Habit(Base):
    __tablename__ = "habit"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    checkin_count = Column(Integer, default=0)
    checkin = relationship("Checkin", back_populates="habit")


class Checkin(Base):
    __tablename__ = "checkin"
    id = Column(Integer, primary_key=True)
    habit_id = Column(Integer, ForeignKey("habit.id"), nullable=False)
    habit = relationship("Habit", back_populates="checkin")
