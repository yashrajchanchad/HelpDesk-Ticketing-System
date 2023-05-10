from django.urls import path

from . import views


app_name = 'it_engineer'

urlpatterns = [
    path('tickets/', views.ticket_list, name='ticket_list'),
    path('update_ticket_Engineer/<int:pk>', views.update_ticket_Engineer, name='update_ticket_Engineer'),
    path('engineergrid/<int:pid>', views.engineergrid , name='engineergrid'),
    path('engineerhome/', views.engineerhome , name='engineerhome')
]