from .models import Ticket
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.utils.html import strip_tags


class TicketEmail:

    def __init__(self,
                 ticket: Ticket, recipients: list,
                 to_self: bool = False, to_engineer: bool = False,
                 to_manager: bool = False
                 ) -> None:
        self.ticket = ticket
        self.sender = settings.DEFAULT_FROM_EMAIL
        self.recipients = recipients
        self.to_self = to_self
        self.to_engineer = to_engineer
        self.to_manager = to_manager

    def send(self, subject=None, body=None) -> None:

        if not subject and not body:
            subject, body = self._get_email_data()

        msg = EmailMultiAlternatives(subject, body, self.sender, self.recipients)
        msg.content_subtype = 'html'
        msg.send()

    def _get_email_data(self) -> tuple:
        if self.to_manager:
            subject = f"New ticket #{self.ticket.id} has been raised."
            message = get_template(
                "email/manager_email.html").render({'ticket': self.ticket})
        elif self.to_engineer:
            subject = f"New ticket #{self.ticket.id} has been raised."
            message = get_template(
                "email/engineer_email.html").render({'ticket': self.ticket})
        else:
            subject = f"Your ticket #{self.ticket.id} has been raised."
            message = get_template(
                "email/user_email.html").render({'ticket': self.ticket})
        return subject, message


def check_valid_status(ticket_status:tuple, action:str):
    '''
    check current action have valid status given in ticket status
    '''
    return any([x for x in ticket_status if action in x])
