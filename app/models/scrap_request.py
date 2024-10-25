from sqlalchemy import Column, Integer, String, ForeignKey, JSON

from app.db.sql import Base
from app.schemas.scrap_request import ScrapRequestStatus


class ScrapRequest(Base):
    __tablename__ = "scrap_requests"

    id = Column(Integer, primary_key=True, index=True)
    user = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), nullable=False)
    page_url = Column(String, nullable=False)
    status = Column(String, nullable=False, default=ScrapRequestStatus.REQUEST_CREATED.value)
    config = Column(JSON)
    data_dump_info = Column(JSON, nullable=True)
