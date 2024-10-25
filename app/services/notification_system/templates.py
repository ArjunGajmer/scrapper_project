from typing import Optional

from pydantic import BaseModel


class BaseNotificationTemplate(BaseModel):
    body: str
    header: Optional[str] = ''

    class Meta:
        abstract = True

    def __str__(self):
        return f"\n\n\t\t\t\t{self.header}\n\n\n\t\t{self.body}"


class EmailNotificationTemplate(BaseNotificationTemplate):
    email: str
    src_email: str


class AppNotificationTemplate(BaseNotificationTemplate):
    user_id: str

