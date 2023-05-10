from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth import get_user_model

from helpdeskapp import forms, models, constants
from helpdeskapp.utils import TicketEmail, check_valid_status
from accounts.decorators import (
    ticket_owner_or_manager_required, ticket_owner_required
)
from helpdeskapp.models import Ticket
from accounts.models import User


User = get_user_model()

@login_required
@ticket_owner_required
def create_ticket(request):
    if request.method == 'POST':
        form = forms.UserTicketForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.raised_by = request.user
            print("instance.raised_by", instance.raised_by)
            instance.save()
            instance.set_history(assigned_by=request.user)
            next = request.POST.get('next')
            manager_emails = [email[0] for email in User.objects.filter(
                is_it_manager=True).values_list('email')]
            # send mail to user
            TicketEmail(
                ticket=instance, recipients=[request.user.email],
                to_self=True
            ).send()

            # send mail to mangers
            TicketEmail(
                ticket=instance, recipients=manager_emails,
                to_manager=True
            ).send()
            return redirect(next if next else request.path)
        context = {'form_errors': form.errors}
        return render(request, 'app/index.html', context)
    next = request.GET.get('next')
    return redirect(next if next else 'helpdeskapp:index')


@ticket_owner_required
def ticket_list(request):
    context = {
        'tickets': models.Ticket.objects.filter(raised_by=request.user),
        'status_choices': constants.TICKET_STATUS,
    }
    return render(request, 'app/getdata.html', context)



@login_required
@ticket_owner_required
def update_ticket_User(request, pk):
    ticket = get_object_or_404(models.Ticket, pk=pk)
    context = {
        'ticket': ticket,
        'form': forms.UserTicketForm(instance=ticket)
    }
    if request.method == 'POST':
        form = forms.UserTicketForm(
            request.POST, request.FILES, instance=ticket)

        if form.is_valid():
            instance = form.save()
            instance.set_history(assigned_by=request.user)
            return redirect('helpdeskapp:ticket_list')
        context['form'] = form
        context['form_errors'] = form.errors
        return render(request, 'app/update_User.html', context)
    return render(request, 'app/update_User.html', context)


def updateRole(request):
    # item = User.objects.all()
    # print("iu", item)

    print("ss", request.user)
    User = get_object_or_404(models.get_user_model(), email= request.user)

    context = {
        'ticket': User,
        'form': forms.UserRoleForm(instance=User)
    }
    if request.method == "POST":
        form = forms.UserRoleForm(
            request.POST, instance=User)

        if form.is_valid():
            instance = form.save()
        context['form'] = form
        context['form_errors'] = form.errors
    return render(request, 'new.html', context)

def grid(request, pid):
    viewtickets = Ticket.objects.get(id=pid)
    return render(request, 'app/grid.html', {"viewtickets": viewtickets})


def edit(request):
    return render(request, 'app/edit.html')


def option(request):
    return render(request, 'app/option.html')


def profile(request):
    item = User.objects.filter(email = request.user).first()
    return render(request, 'profile.html' ,{'first_name': item.first_name,'Title':item.job_title ,'phone_number':item.phone_number, 'last_name':item.last_name,'department':item.department , 'email':item, 'city':item.city})

def base(request):
    item = User.objects.filter(email = request.user).first()
    return render(request, 'base.html' ,{'first_name': item.first_name,'Title':item.job_title ,'phone_number':item.phone_number, 'last_name':item.last_name,'department':item.department , 'email':item, 'city':item.city})


def welcome(request):
    return render(request, 'app/welcome.html')


@login_required
@ticket_owner_required # *ticket_owner_required
def change_ticket_status(request):
    if request.method == 'POST':
        status = request.POST.get('status')
        ticket_id = request.POST.get('ticket_id')

        ticket = get_object_or_404(models.Ticket, pk=int(ticket_id))
        
        if not check_valid_status(constants.USER_TICKET_STATUS, status): # *USER_TICKET_STATUS
            '''user does not have permission to perform status update'''
            return redirect(reverse('helpdeskapp:grid', args=[ticket.id])) # *helpdeskapp:grid
        
        ticket.status = status
        ticket.save()
        ticket.set_history(assigned_by=request.user)
        # send success message of status update
        return redirect(reverse('helpdeskapp:grid', args=[ticket.id])) # *helpdeskapp:grid
    # redirecting user on GET becouse we've not implemented this part
    return redirect(reverse('helpdeskapp:grid', args=[ticket.id])) # *helpdeskapp:grid


def ticket_history(request, ticket_id):
    history = models.TicketHistory.objects.filter(ticket__id=ticket_id)
    return render(request, "app/history.html", {"ticket_history":history})

def home(request):
    return render(request, 'home.html')