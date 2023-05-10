from django.http import HttpRequest
from django.contrib import admin
from .models import Ticket, TicketHistory


class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'ticketType',  'department')
    list_display_links = ('id', 'title', 'ticketType', 'department')

    def save_model(self, request: HttpRequest, obj: Ticket, form: any, change: any) -> None:
        super().save_model(request, obj, form, change)
        obj.set_history(assigned_by=request.user)


class TicketHistoryAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'ticket', 'status', 'assigned_by',
    )
    list_display_links = (
        'id', 'ticket', 'status', 'assigned_by'
    )


admin.site.register(Ticket, TicketAdmin)
admin.site.register(TicketHistory, TicketHistoryAdmin)
