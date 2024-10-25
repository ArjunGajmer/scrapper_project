import logging

from app.services.notification_system import Notifier
from app.services.notification_system.templates import AppNotificationTemplate


class InAppNotifier(Notifier):
    template_class = AppNotificationTemplate

    def generate_notification_template(self):
        return self.template_class(
            header=self.header,
            body=self.body,
            user_id=str(self.user.id)
        )

    def notify(self):
        notification_template = self.generate_notification_template()
        print(f"{notification_template}")
        logging.info(f"{notification_template}")
        return f"{notification_template}"
