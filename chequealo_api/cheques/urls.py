from django.urls import path
from .views import ProcesarChequeView

urlpatterns = [
    path('procesar/', ProcesarChequeView.as_view(), name='procesar-cheque'),
]
