from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from config.db import Base
from models.player import Player

class Team(Base):
    __tablename__ = 'teams'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    city = Column(String)
    coach = Column(String)
    established_year = Column(DateTime)

    # Define the relationship to Player
    players = relationship("Player", back_populates="team", cascade="all, delete")

    def __repr__(self):
        return f"<Team(id={self.id}, name={self.name}, city={self.city})>"
