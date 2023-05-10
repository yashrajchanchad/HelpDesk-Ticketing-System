from django.shortcuts import render


import json

from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from helpdeskapp.forms import EngineerTicketForm

from helpdeskapp import forms, models, constants
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from helpdeskapp.utils import TicketEmail
from helpdeskweb.settings import EMAIL_HOST_USER
from accounts.decorators import (
    ticket_owner_or_manager_required, ticket_owner_required
)
from helpdeskapp.models import Ticket
# send mail function
from django.shortcuts import render

from accounts.decorators import it_engineer_required

from helpdeskapp.models import Ticket
# Create your views here.


User = get_user_model()


@login_required
@it_engineer_required
def ticket_list(request):
    tickets = Ticket.objects.filter(assign_to=request.user)
    context = {'tickets': tickets}
    return render(request, 'engineer/ticket_list.html', context)



@login_required
@it_engineer_required
def update_ticket_Engineer(request, pk):
    #Todo add manager filtering to update queryset
    ticket = get_object_or_404(models.Ticket, pk=pk)
    context = {
        'ticket': ticket,
        'form': forms.EngineerTicketForm(instance=ticket)
    }
    if request.method == 'POST':
        form = forms.EngineerTicketForm(request.POST, request.FILES, instance=ticket)
        

        if form.is_valid():
            form.save()
            return redirect('it_engineer:ticket_list')
        context['form'] = form
        context['form_errors'] = form.errors
        return render(request, 'engineer/update_Engineer.html', context)
    return render(request, 'engineer/update_Engineer.html', context)


def engineergrid(request,pid):
    viewtickets=Ticket.objects.get(id=pid)
    return render(request,'engineer/engineergrid.html',{"viewtickets":viewtickets})


def engineerhome(request):
    return render(request ,'app/components/home/it_engineer_home.html' )