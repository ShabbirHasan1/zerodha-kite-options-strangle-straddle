from django.urls import path
from .views import login, dashboard, logout

urlpatterns = [
    path('login/', login, name='login'),
    path('', dashboard, name='dashboard'),
    path('logout/', logout, name='logout'),
]
