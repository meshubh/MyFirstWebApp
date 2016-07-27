from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
import views

urlpatterns = [
    url(r'^api/restaurantlist/$', views.restaurant_list),
    url(r'^api/restaurantsowner/$', views.restaurant_list_owner),
    url(r'^api/restaurantlist/(?P<pk>[0-9]+)$', views.restaurant_detail),
    url(r'^api/restaurantlist/(?P<lid>[0-9]+)/menu/$', views.menu_list),
    url(r'^api/restaurantlist/(?P<lid>[0-9]+)/menu/(?P<pk>[0-9]+)$', views.menu_detail),
    url(r'^api/menu/$', views.menu_all_item),
    url(r'^api/menu/(?P<pk>[0-9]+)$', views.menu_detail),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login),
    url(r'^logout/$', views.user_logout, name='logout'),
]