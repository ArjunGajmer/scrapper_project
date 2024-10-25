import abc

from app.models import User
from app.services.notification_system.templates import BaseNotificationTemplate


class Notifier(abc.ABC):
    template_class = BaseNotificationTemplate

    def __init__(self, user: User, header: str, body: str):
        self.user: User = user
        self.body: str = body
        self.header: str = header

    @abc.abstractmethod
    def generate_notification_template(self):
        # each sub class will have different implementation
        pass

    @abc.abstractmethod
    def notify(self):
        # each sub class will have different implementation
        pass
