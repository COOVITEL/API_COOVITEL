from rest_framework import serializers
from .models import *


class PagaduriasSerializer(serializers.ModelSerializer):
    class Meta:
        model = PagaduriasLinix
        fields = '__all__'