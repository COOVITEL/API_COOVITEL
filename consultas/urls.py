from django.urls import path
from .views import *

urlpatterns = [
    path('asociado/<str:cedula>', consulta_asociado, name='consultar_asociado'),
    path('pagadurias/', PagaduriasLinixApiView.as_view(), name='consultar_pagadurias'),
    path('crear-pagadurias/', crear_pagadurias, name='crear_pagadurias'),
]
