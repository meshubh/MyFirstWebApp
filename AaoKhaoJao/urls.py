from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
import views,classviews

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
    url(r'^secondpage/$', views.second_home),
    url(r'^editmenu/(?P<id>[0-9]+)$', views.manage_restaurants),
    url(r'^allrestaurants/$', views.order_restaurants),
    url(r'^confirmorder/$', views.confirm_order),
    url(r'^restaurant/create', view=classviews.restaurantcreateview.as_view(), name="addrestaurant"),
    url(r'^restaurant/(?P<pk>[0-9]+)/update', view=classviews.restaurantupdateview.as_view(), name="updaterestaurant"),
    url(r'^restaurant/(?P<pk>[0-9]+)/delete', view=classviews.restaurantdeleteview.as_view(), name="deleterestaurant"),
    url(r'^ownersrestaurant/$', views.restaurant_owners),
    url(r'^restaurantsowned/$', view=classviews.list, name="list"),
    url(r'^menu/(?P<pk>[0-9]+)/$', view=classviews.menucreateview.as_view(), name="addmenu"),
    url(r'^menu/(?P<id>[0-9]+)/menu/(?P<pk>[0-9]+)/update/$', view=classviews.menuupdateview.as_view(), name="updatemenuitem"),
    url(r'^menu/(?P<id>[0-9]+)/menu/(?P<pk>[0-9]+)/delete/$', view=classviews.menudeleteview.as_view(), name="deletemenu"),
    url(r'^editmenu/(?P<pk>[0-9]+)/$', view=classviews.menus, name="posts")
]