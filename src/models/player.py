from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from config.db import Base

class Player(Base):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    position = Column(String)
    team_id = Column(Integer, ForeignKey('teams.id'))

    team = relationship("Team", back_populates="players")
    injuries = relationship("Injury", back_populates="player")
    performances = relationship("Performance", back_populates="player")

    def __repr__(self):
        return f"<Player(id={self.id}, name={self.name}, position={self.position})>"
