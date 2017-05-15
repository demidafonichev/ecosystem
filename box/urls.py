from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^get_plants/', views.get_plants),
    url(r'^check_key_and_name/', views.check_key_and_name),
    url(r'^save_box/', views.save_box),
    url(r'^get_box_list/', views.get_box_list),
    url(r'^change_box/', views.change_box),
    url(r'^delete_box/', views.delete_box),
]
