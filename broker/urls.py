from django.urls import path
from .views import kite_set_access_token

urlpatterns = [
    path('kite-login/', kite_set_access_token, name='kite-login'),
]
