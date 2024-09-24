from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from config.db import Base

class ExternalFactor(Base):
    __tablename__ = 'external_factors'

    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey('games.id'))
    team_id = Column(Integer, ForeignKey('teams.id'))
    factor_type = Column(String)
    description = Column(Text)
    impact = Column(Integer)
    recorded_at = Column(DateTime)

    def __repr__(self):
        return f"<ExternalFactor(team_id={self.team_id}, game_id={self.game_id}, factor_type={self.factor_type})>"
