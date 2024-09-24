from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from config.db import Base

class ExternalFactor(Base):
    __tablename__ = 'external_factors'

    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey('games.id'))
    factor_type = Column(String)
    description = Column(String)

    game = relationship("Game", back_populates="external_factors")
