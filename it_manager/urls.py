from django.urls import path

from . import views


app_name = 'it_manager'

urlpatterns = [
    path('tickets/', views.ticket_list, name='ticket_list'),
    path('update_ticket_manager/<int:pk>', views.update_ticket_manager, name='update_ticket_manager'),
    path('manager-grid/<int:pid>/', views.manager_grid, name='manager_grid'),
    path('change-ticket-status/', views.change_ticket_status, name='change_ticket_status'),


    # path('grid/', views.grid, name='grid'),

]