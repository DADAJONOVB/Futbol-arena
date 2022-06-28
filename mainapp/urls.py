from django.urls import path
from .views import *

urlpatterns= [
    path('', index_view, name='dashboard_url' ),
    path('turnir/', turnir_view, name='turnir_url'),
    path('tur/<int:pk>/', turnir_tur_view, name='tur_url')
]