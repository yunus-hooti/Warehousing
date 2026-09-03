from django.urls import path
from . import views

app_name = 'supplier'

urlpatterns = [
    path('list_supplier/',views.list_suppliers,name='list_supplier'),
    path('detail_supplier/<int:pk>',views.detail_supplier,name='detail_supplier'),
    path('send_supplier/',views.send_supplier,name='send_supplier'),
]