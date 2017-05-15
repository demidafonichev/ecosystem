from django.conf.urls import url, include
from django.contrib.auth.views import login, logout
from . import views

from .forms import UserAuthenticationForm


urlpatterns = [
    url(r'^$', login, {'template_name': 'login.html', 'authentication_form': UserAuthenticationForm}, name='login'),
    url(r'^logout/', logout, {'next_page': '/'}),
    url(r'^profile/', views.profile, name='profile'),
    url(r'^register', views.register, name='register')
]
