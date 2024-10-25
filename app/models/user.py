import enum

from sqlalchemy import Column, Integer, String

from app.db.sql import Base


class UserNotificationPreference(enum.Enum):
    email = 'email'
    sms = 'sms'
    in_app = 'app'


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    notification_preference = Column(String, nullable=False, default=UserNotificationPreference.in_app.value )
