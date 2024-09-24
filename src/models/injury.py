from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
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
    recorded_at = Column(DateTime)

    player = relationship("Player", back_populates="injuries")
    game = relationship("Game", back_populates="injuries")

    def __repr__(self):
        return f"<Injury(player_id={self.player_id}, game_id={self.game_id}, injury_type={self.injury_type})>"
