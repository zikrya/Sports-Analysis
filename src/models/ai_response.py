from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from config.db import Base

class AIResponse(Base):
    __tablename__ = 'ai_responses'

    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey('teams.id'))
    response_text = Column(Text)
    category = Column(String)
    generated_at = Column(DateTime)

    def __repr__(self):
        return f"<AIResponse(team_id={self.team_id}, category={self.category}, generated_at={self.generated_at})>"
