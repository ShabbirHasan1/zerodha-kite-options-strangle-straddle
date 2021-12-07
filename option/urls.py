from django.urls import path
from . views import strategy_list_view, strategy_create_view, strategy_update_view
urlpatterns = [
    path('strategy/list/', strategy_list_view, name='strategy_list'),
    path('strategy/create/', strategy_create_view, name='strategy_create'),
    path('strategy/update/<int:pk>', strategy_update_view, name='strategy_update'),
]
