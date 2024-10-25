import logging

from app.config import settings
from app.services.notification_system import Notifier
from app.services.notification_system.templates import EmailNotificationTemplate


class EmailNotifier(Notifier):
    template_class = EmailNotificationTemplate

    def generate_notification_template(self):
        return self.template_class(
            header=self.header,
            body=self.body,
            email=self.user.email,
            src_email=settings.EMAIL_NOTIFICATION_SRC
        )

    def notify(self):
        notification_template = self.generate_notification_template()
        print(f"{notification_template}")
        logging.info(f"{notification_template}")
