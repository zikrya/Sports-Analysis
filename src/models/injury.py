from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from config.db import Base

class Injury(Base):
    __tablename__ = 'injuries'

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey('players.id'))
    game_id = Column(Integer, ForeignKey('games.id'))
    injury_type = Column(String)
    severity = Column(String)
    recovery_time = Column(Integer)

    player = relationship("Player", back_populates="injuries")
    game = relationship("Game")
