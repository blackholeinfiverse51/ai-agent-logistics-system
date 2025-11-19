from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class AuditLog(Base):
    __tablename__ = 'audit_logs'
    
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    user = Column(String(100), index=True)
    action = Column(String(50), index=True)
    resource = Column(String(100))
    resource_id = Column(String(100))
    status = Column(String(20))
    ip_address = Column(String(50))
    user_agent = Column(String(200))
    details = Column(Text)
