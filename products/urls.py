from django.urls import path
from rest_framework.authtoken import views
from .views import Products, UserProducts

urlpatterns = [
    # products 
    path('admin/records', Products.as_view({'get': 'records'})),
    path('admin/record/<str:id>', Products.as_view({'get': 'record'})),
    path('admin/revenue', Products.as_view({'get': 'get_total_revenue'})),
    path('admin/create', Products.as_view({'post': 'create'})),
    path('admin/delete/<str:id>', Products.as_view({'delete': 'delete'})),
    path('admin/update/<str:id>', Products.as_view({'put': 'update'})),
    
    path('user/records/<str:currency>', UserProducts.as_view({'get': 'records'})),
    path('user/purchased/records/<str:currency>', UserProducts.as_view({'get': 'purchased_records'})),
    path('user/record/<str:id>/<str:currency>', UserProducts.as_view({'get': 'record'})),
    path('user/purchase', UserProducts.as_view({'post': 'purchase'})),
]
