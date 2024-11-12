from rest_framework import serializers
from .models import Tila, Varaaja, Varaus

class TilaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tila
        fields = '__all__'

class VaraajaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Varaaja
        fields = '__all__'

class VarausSerializer(serializers.ModelSerializer):
    class Meta:
        model = Varaus
        fields = '__all__'
