from rest_framework import serializers
from AaoKhaoJao.models import *

class RestaurantsSerializer(serializers.ModelSerializer):
    class Meta:
            model = Restaurants
            fields = ('name','location','id','owner')

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
            model = Menu
            fields = ('item', 'price','restaurant_id','id')