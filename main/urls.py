# django imports
from django.urls import path

# folder imports
from .views import GreendeckData, GreendeckDataAction


# urls
urlpatterns = [
    path('data_get_create', GreendeckData.as_view(), name='data_get_create'),
    path('data_action/<pk>', GreendeckDataAction.as_view(), name='data_action')
]