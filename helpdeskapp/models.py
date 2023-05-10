from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

from helpdeskapp import constants
# Create your models here.


class Ticket(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    contact_number = models.PositiveIntegerField(blank=True, null=True)
    ticketType = models.CharField(max_length=100)
    ticketSubType = models.CharField(max_length=100)
    attachment = models.FileField(upload_to='files')
    priority = models.CharField(
        choices=constants.PRIORITY, max_length=100, default='low', blank=True, null=True)
    department = models.CharField(
        choices=constants.DEPARTMENT, max_length=100, blank=True, null=True)
    status = models.CharField(
        choices=constants.TICKET_STATUS, max_length=10, default='open', blank=True, null=True)
    raised_by = models.ForeignKey(
        get_user_model(), on_delete=models.DO_NOTHING, related_name='tickets', null=True, blank=True)
    assign_to = models.ForeignKey(
        get_user_model(), on_delete=models.DO_NOTHING, related_name='assigned_tickets', null=True, blank=True)

    def get_status_options(self):
        return constants.TICKET_STATUS

    def set_history(self, **kwargs) -> None:
        t = TicketHistory.objects.filter(ticket=self)
        if not t.exists():
            t = TicketHistory(
                ticket=self,
                status=self.status,
                assigned_to=self.assign_to,
                assigned_by=kwargs.get('assigned_by'),
            )
            t.save()
        else:
            t = t.first()
            t.status = self.status
            t.assigned_to=self.assign_to
            t.assigned_by=kwargs.get('assigned_by')
            t.save()


class TicketHistory(models.Model):
    ticket = models.ForeignKey(
        Ticket, on_delete=models.CASCADE, related_name='assignments')
    status = models.CharField(
        choices=constants.TICKET_STATUS, max_length=10, blank=True, null=True)
    assigned_to = models.ForeignKey(
        get_user_model(), on_delete=models.DO_NOTHING, related_name='tickets_assigned_to', null=True, blank=True)
    assigned_by = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name='tickets_assigned_by')
    assigned_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    time_to_resolve = models.DurationField(null=True, blank=True)
    # time_to_close = models.DurationField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.status} ticket id {self.ticket.id}"

    def save(self, *args, **kwargs):

        if self.status == 'closed':
            self.completed_at = timezone.now()

        if self.status == "open" and self.time_to_resolve:
            # reset all time if user opens ticket again
            self.time_to_resolve = None
            self.assigned_at = timezone.now()
            self.completed_at = None

        if self.completed_at and self.assigned_at and not self.time_to_resolve:
            # updating time to resolve after ticket is completed
            self.time_to_resolve = self.completed_at-self.assigned_at

        super(TicketHistory, self).save(*args, **kwargs)
