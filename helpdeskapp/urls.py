from django.urls import path
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from helpdeskapp import views


app_name = 'helpdeskapp'

urlpatterns = [
    path('',views.home, name='home'),
    path('login/', login_required(TemplateView.as_view(
        template_name='app/index.html')), name='index'),
    path('create-ticket/', views.create_ticket, name='create_ticket'),
    path('view-tickets/', views.ticket_list, name='ticket_list'),
    path('update-ticket/<pk>/', views.update_ticket_User, name='update_ticket_User'),
    path('change-ticket-status/', views.change_ticket_status, name='change_ticket_status'),
    path('grid/<int:pid>/', views.grid, name='grid'),
    path('edit/', views.edit, name='edit'),
    path('option/', views.option, name='option'),
    path('profile/', views.profile, name='profile'),
    path('welcome/',views.welcome,name='welcome'),
    path('history/<int:ticket_id>/',views.ticket_history,name='ticket_history'),
    path('updateRole/', views.updateRole , name="updateRole"),
    path('base/',views.base,name='base')
    
]
 