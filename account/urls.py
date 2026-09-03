from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'account'
urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('registration/', views.registration, name='registration'),
    path('profile/', views.profile, name='profile'),
    path('password_reset/', auth_views.PasswordResetView.as_view(success_url='done',
                                                                 email_template_name='reqistration/password_reset_email.html',
                                                                 template_name='reqistration/password_reset_form.html',),
         name='password_resetView'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='reqistration/password_reset_done.html'), name='PasswordResetDone'),
    path('password_reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='reqistration/password_reset_confirm.html',success_url='done'),
         name='password_reset_confirm'),
    path('password_reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='PasswordResetCompleteView'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='reqistration/password_change_form.html',success_url='done'), name='PasswordChangeView'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='reqistration/password_change_done.html'), name='PasswordChangeDoneView'),
]
