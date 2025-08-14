from rest_framework import serializers
from .models import Prism

class PrismSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prism
        fields = '__all__'
