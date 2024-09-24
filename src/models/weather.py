from xmlrpc.client import DateTime
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from config.db import Base

class Weather(Base):
    __tablename__ = 'weather'

    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey('games.id'))
    condition = Column(String)
    temperature = Column(Integer)
    wind_speed = Column(Integer)
    recorded_at = Column(DateTime)

    game = relationship("Game", back_populates="weather")

    def __repr__(self):
        return f"<Weather(game_id={self.game_id}, condition={self.condition}, temperature={self.temperature})>"
