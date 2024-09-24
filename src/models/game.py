from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from config.db import Base

class Game(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime)
    home_team_id = Column(Integer, ForeignKey('teams.id'))
    away_team_id = Column(Integer, ForeignKey('teams.id'))
    home_score = Column(Integer)
    away_score = Column(Integer)

    home_team = relationship("Team", foreign_keys=[home_team_id], back_populates="home_games")
    away_team = relationship("Team", foreign_keys=[away_team_id], back_populates="away_games")
    injuries = relationship("Injury", back_populates="game")
    performances = relationship("Performance", back_populates="game")
    weather = relationship("Weather", back_populates="game")
    external_factors = relationship("ExternalFactor", back_populates="game")

    def __repr__(self):
        return f"<Game(id={self.id}, date={self.date}, home_team_id={self.home_team_id}, away_team_id={self.away_team_id})>"
