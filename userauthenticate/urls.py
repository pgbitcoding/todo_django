from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('task/forgot/', views.forgot_password, name='forgot_passord'),
    path('task/change_password/', views.change_password, name='change_password'),
    path('task/profile/', views.profile, name='profile'),
    path('reset-password/<int:uid>/<str:token>', views.reset_password, name='password_reset_done'),
    path('activate/<str:uidb64>/<str:token>/', views.activate, name='activate'),
]