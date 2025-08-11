from rest_framework import serializers
from .models import ChequeProcesado

class ChequeProcesadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChequeProcesado
        fields = '__all__'
