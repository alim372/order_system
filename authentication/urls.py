from django.urls import path
from rest_framework.authtoken import views
from .views import Auth, Profile

urlpatterns = [
    # auth
    path('login', Auth.as_view({'post': 'login'}), name='login'),
    path('signup', Auth.as_view({'post': 'signup'}), name='signup'),
    # profile
    path('changePassword', Profile.as_view({'post': 'changePassword'}), name='changePassword'),
    path('logout', Profile.as_view({'get': 'logout'}), name='logout'),
]
