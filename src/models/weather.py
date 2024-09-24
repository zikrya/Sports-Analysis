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

    game = relationship("Game", back_populates="weather")
