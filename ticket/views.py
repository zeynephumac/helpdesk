from cgitb import reset
import datetime
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.contrib import messages
from ticket.models import Ticket
from .form import CreatTicketForm, UpdateTicketForm, SolutionForm
from users.models import User
from django.contrib.auth.decorators import login_required



# view ticket details
@login_required
def ticket_details(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    t = User.objects.get(username=ticket.created_by)
    tickets_per_user = t.created_by.all()
    context = {'ticket':ticket, 'tickets_per_user' : tickets_per_user}
    return render(request, 'ticket/ticket_details.html', context)


"""For Customers"""
# creating a ticket
@login_required
def create_ticket(request):
    if request.method == 'POST':
        form = CreatTicketForm(request.POST)
        if form.is_valid():
            var = form.save(commit=False)
            var.created_by = request.user
            var.ticket_status = 'Pending'
            var.save()
            messages.success(request, 'Your ticket has been succesfully submitted. A manager would be assigned soon')
            return redirect('dashboard')
        else:
            messages.warning(request, 'Something went wrong. Please check form input')
            return redirect('create-ticket')
    else:
        form = CreatTicketForm()
        context = {'form':form}
        return render(request, 'ticket/create_ticket.html', context)
    
    
# updating a ticket
@login_required
def update_ticket(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    if not ticket.is_resolved : 
        if request.method == 'POST':
            form = UpdateTicketForm(request.POST, instance=ticket)
            if form.is_valid():
                form.save()
                messages.info(request, 'Your ticket info has been updated and all changes are saved in the Database')
                return redirect('dashboard')
            else:
                messages.warning(request, 'Something went wrong. Please check form input')
                #return redirect('create-ticket')
        else:
            form = UpdateTicketForm(instance=ticket)
            context = {'form':form}
            return render(request, 'ticket/update_ticket.html', context)
    else:
        messages.warning(request, 'You cannot make any changes')   
        return redirect('dashboard')


# viewing all created tickets
@login_required
def all_tickets(request):
    tickets = Ticket.objects.filter(created_by=request.user).order_by('-date_created')
    context = {'tickets' :tickets}
    return render(request, 'ticket/all_tickets.html', context)


"""For Managers"""

#view ticket queue
@login_required
def ticket_queue(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    filtered_tickets = Ticket.objects.filter(ticket_status='Pending')

    if start_date and end_date:
        filtered_tickets = filtered_tickets.filter(date_created__range=[start_date, end_date])

    context = {'filtered_tickets': filtered_tickets}
    return render(request, 'ticket/ticket_queue.html', context)    


#accept a ticket from the queue
@login_required
def accept_ticket(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    ticket.assigned_to = request.user
    ticket.ticket_status = 'Active'
    ticket.accepted_date = datetime.datetime.now()
    ticket.save()
    messages.info(request, 'Ticket has been accepted. Please resolve as soon as possible!')
    return redirect('workspace')


@login_required
def solution(request, pk):
    ticket = Ticket.objects.get(pk=pk)

    if not ticket.is_resolved: 
        if request.method == 'POST':
            form = SolutionForm(request.POST, instance=ticket)
            if form.is_valid():
                form.save()
                messages.info(request, 'Your solution has been submitted')
                return redirect('ticket-details', pk=pk)
            else:
                messages.warning(request, 'Something went wrong. Please check form input')
        else:
            form = SolutionForm(instance=ticket)
        
        context = {'form': form, 'ticket': ticket}
        return render(request, 'ticket/solution.html', context)
    else:
        messages.warning(request, 'You cannot make any changes')   
        return redirect('dashboard')
                
                

# close a ticket 
@login_required
def close_ticket(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    ticket.ticket_status = 'Completed'
    ticket.is_resolved = True
    ticket.closed_date = datetime.datetime.now()
    ticket.save()
    messages.info(request, 'Ticket has been resolved. Thank you brilliant Support Manager')
    return redirect('ticket-queue')


# tickets manager is working on
@login_required
def workspace(request):
    tickets = Ticket.objects.filter(
        assigned_to=request.user,
        is_resolved=False)
    context = {'tickets':tickets}
    return render(request, 'ticket/workspace.html', context)


# all closed/resolved tickets
@login_required
def all_closed_tickets(request):
    tickets = Ticket.objects.filter(assigned_to = request.user, is_resolved = True)
    context = {'tickets':tickets}
    return render(request, 'ticket/all_closed_tickets.html', context)


@login_required
def locked_accounts(request):
    if request.user.is_manager:
        locked_users = User.objects.filter(is_active=False, is_manager=False)
        context = {'locked_users': locked_users}
        return render(request, 'ticket/locked_accounts.html', context)
    else:
        return HttpResponseForbidden("You don't have permission to view locked user accounts.")


@login_required
def activate_account(request, user_id):
    if request.user.is_manager:
        user = User.objects.get(id=user_id)
        if not user.is_manager:
            user.is_active = True
            user.save()
            messages.info(request, f'{user.username}\'s account is now activated.')
            user.login_attempts = 0
            user.save()
        else:
            messages.warning(request, 'Manager accounts cannot be activated.')
        return redirect('locked-accounts')
    else:
        return HttpResponseForbidden("You don't have permission to activate user accounts.")
