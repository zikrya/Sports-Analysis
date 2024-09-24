from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from config.db import Base

class Performance(Base):
    __tablename__ = 'performances'

    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey('games.id'))
    player_id = Column(Integer, ForeignKey('players.id'))
    metric_name = Column(String)
    metric_value = Column(Integer)
    recorded_at = Column(DateTime)

    player = relationship("Player", back_populates="performances")
    game = relationship("Game", back_populates="performances")

    def __repr__(self):
        return f"<Performance(player_id={self.player_id}, game_id={self.game_id}, metric_name={self.metric_name})>"
