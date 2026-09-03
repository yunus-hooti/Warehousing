from django.urls import path
from . import views

app_name = 'goods'
urlpatterns = [
    path('list_goods/',views.list_goods,name='list_goods'),
    path('detail_good/<int:goods_id>/',views.detail_goods,name='detail_good'),
    path('search_goods/',views.search_goods,name='search_goods'),
    path('list_filtered/<str:filtered>/',views.list_goods,name='list_filtered'),
    path('add_goods/',views.add_goods,name='add_goods'),
    path('add_categories/',views.add_categories,name='add_categories'),
    path('',views.dashboard_view,name='dashboard_view'),
]
