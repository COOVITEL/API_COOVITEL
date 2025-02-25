from django.urls import path
from .views import consulta_asociado

urlpatterns = [
    path('asociado/<str:cedula>', consulta_asociado, name='consultar_asociado'),
]
