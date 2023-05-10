from django.shortcuts import render
from helpdeskapp.utils import TicketEmail, check_valid_status
from django.contrib.auth import get_user_model

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from helpdeskapp import constants, forms, models
from helpdeskapp.models import Ticket
# send mail function
from accounts.decorators import it_manager_required

from helpdeskapp.models import Ticket
from django.urls import reverse

# Create your views here.

User = get_user_model()

@login_required
@it_manager_required
def ticket_list(request):
    tickets = Ticket.objects.all()
    context = {'tickets': tickets}
    return render(request, 'manager/ticket_list.html', context)


@login_required
@it_manager_required
def update_ticket_manager(request, pk):
    ticket = get_object_or_404(models.Ticket, pk=pk)
    context = {
        'ticket': ticket,
        'form': forms.ManagerTicketForm(instance=ticket)
    }
    if request.method == 'POST':
        form = forms.ManagerTicketForm(request.POST, request.FILES, instance=ticket)

        if form.is_valid():
            instance = form.save()
            instance.set_history(assigned_by=request.user)
            print("engineer", instance.raised_by)
            
            engineer_emails = [email[0] for email in User.objects.filter(                
                is_it_engineer=True,email= instance.assign_to ).values_list('email')]
            TicketEmail(
                ticket=instance,recipients=engineer_emails,
                to_engineer=True
            ).send()
            TicketEmail(
            ticket=instance, recipients=[instance.raised_by],
            to_self=True
            ).send()
            return redirect('it_manager:ticket_list')
        context['form'] = form
        context['form_errors'] = form.errors
        return render(request, 'manager/update_manager.html', context)
    return render(request, 'manager/update_manager.html', context)


def manager_grid(request,pid):
    viewtickets=Ticket.objects.get(id=pid)
    return render(request,'manager/managergrid.html',{"viewtickets":viewtickets})


@login_required
@it_manager_required # *ticket_owner_required
def change_ticket_status(request):
    if request.method == 'POST':
        status = request.POST.get('status')
        ticket_id = request.POST.get('ticket_id')

        ticket = get_object_or_404(models.Ticket, pk=int(ticket_id))
        
        if not check_valid_status(constants.MANAGER_TICKET_STATUS, status): # *USER_TICKET_STATUS
            '''user does not have permission to perform status update'''
            return redirect(reverse('it_manager:manager_grid', args=[ticket.id])) # *helpdeskapp:grid
        
        ticket.status = status
        ticket.save()
        ticket.set_history(assigned_by=request.user)
        # send success message of status update
        return redirect(reverse('it_manager:manager_grid', args=[ticket.id])) # *helpdeskapp:grid
    # redirecting user on GET becouse we've not implemented this part
    return redirect(reverse('it_manager:manager_grid', args=[ticket.id])) # *helpdeskapp:grid
