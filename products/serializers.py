from rest_framework import serializers
from django.conf import settings
# models
from .models import Product, UserProduct

""""""""""""""""""""""""""""""
# Product serialzer.
""""""""""""""""""""""""""""""
class ProductSerializer(serializers.ModelSerializer):
    user_currancy_price = serializers.SerializerMethodField() # add field
    def get_user_currancy_price(self, obj):
        # here write the logic to compute the value based on object
        return obj.price_eur

    class Meta:
        model = Product
        fields = '__all__'

""""""""""""""""""""""""""""""
# User Product serialzer.
""""""""""""""""""""""""""""""
class UserProductSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(required=False)
    product = ProductSerializer(many=False)
    
    class Meta:
        model = UserProduct
        fields = '__all__'