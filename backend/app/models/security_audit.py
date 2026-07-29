# Copyright (c) 2026 Chinmay Hudedamani. All Rights Reserved.
# APEX AI / Copus AI — Security Firewall Audit Log Model

from sqlalchemy import Column, String, DateTime, Text
from datetime import datetime
from app.models.pro_tier import Base


class SecurityAuditLog(Base):
    __tablename__ = "security_audit_logs"

    id = Column(String(50), primary_key=True)
    ip_address = Column(String(45), nullable=False)
    endpoint = Column(String(255), nullable=False)
    method = Column(String(10), nullable=False)
    violation_type = Column(String(50), nullable=False)  # SQLI, XSS, RATE_LIMIT, FORBIDDEN
    payload_snippet = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
