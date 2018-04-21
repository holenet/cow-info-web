from rest_framework import serializers

from cowapp.models import Cow


class CowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cow
        fields = ('id', 'created', 'number', 'sex', 'birthday', 'mother')
