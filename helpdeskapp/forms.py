from django import forms
from django.contrib.auth import get_user_model

from helpdeskapp import models
from helpdeskapp.constants import USER_TICKET_STATUS, MANAGER_TICKET_STATUS, ENGINEER_TICKET_STATUS


User = get_user_model()

class UserTicketForm(forms.ModelForm):
    status = forms.ChoiceField(choices=USER_TICKET_STATUS, widget=forms.Select(),required=False)
    class Meta:
       model = models.Ticket
       fields = ['title', 'description', 'contact_number', 'ticketType' , 'ticketSubType','attachment','priority','department','status']


class ManagerTicketForm(forms.ModelForm):
    status = forms.ChoiceField(choices=MANAGER_TICKET_STATUS, widget=forms.Select())
    assign_to = forms.ModelChoiceField(queryset=User.objects.filter(is_it_engineer=True))
    class Meta:
       model = models.Ticket
       fields = ['title', 'description', 'contact_number', 'ticketType' , 'ticketSubType','attachment','priority','department','status','assign_to']


class EngineerTicketForm(forms.ModelForm):
    status = forms.ChoiceField(choices=ENGINEER_TICKET_STATUS, widget=forms.Select())
    class Meta:
       model = models.Ticket
       fields = ['status']

class UserRoleForm(forms.ModelForm):
    class Meta:
        model = models.get_user_model()
        fields = ['is_it_manager','is_it_engineer']