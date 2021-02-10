from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('parties/', views.parties, name='parties'),
    path('party/<int:party_id>/', views.party, name='party'),
    path('create_party/', views.create_party, name='create_party'),
    path('edit_party/<int:party_id>/', views.edit_party, name='edit_party'),
    path('user/<int:user_id>/', views.user, name='user'),
    path('', views.index, name='index')
]