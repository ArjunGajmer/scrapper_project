from typing import Type

from app.models import User
from app.models.user import UserNotificationPreference
from app.services.notification_system.base_notifier import Notifier
from app.services.notification_system.in_app import InAppNotifier
from app.services.notification_system.email import EmailNotifier


def get_notifier(user: User) -> Type[Notifier]:
    if user.notification_preference == UserNotificationPreference.in_app.value:
        return InAppNotifier

    if user.notification_preference == UserNotificationPreference.email.value:
        return EmailNotifier
