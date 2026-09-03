from django.urls import path
from . import views

app_name = 'entry_exit'

urlpatterns = [
    path('entry_exit_entry/',views.entry_exit_entry,name='entry_exit_entry'),
    path('entry_exit_exit/',views.entry_exit_exit,name='entry_exit_exit'),
    path('list_entry_exit/',views.list_entry_exit,name='list_entry_exit'),
    path('list_entry_exit_filters/<str:filter>/',views.list_entry_exit,name='list_entry_exit_filters'),
    path('detail_entry_exit/<int:entry_id>/',views.detail_entry_exit,name='detail_entry_exit'),
    path('search_goods/', views.search_goods, name='search_goods'),
    path('pdf_receipt/<int:pk>/',views.generate_pdf_receipt,name='pdf_receipt'),
    path('ajax/load-suppliers/', views.load_suppliers_for_good, name='ajax_load_suppliers'),
    path('entry_exit/is_active/<int:entry_exit_id>/',views.true_is_good_entry_exit,name='true_is_good_entry_exit'),

]