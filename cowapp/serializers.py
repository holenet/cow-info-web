from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from cowapp.models import Cow, Record


class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        exclude = ('user',)


class CowSerializer(serializers.ModelSerializer):
    sex = serializers.ChoiceField(choices=[('female', 'female'), ('male', 'male')])
    records = RecordSerializer(many=True, read_only=True)

    class Meta:
        model = Cow
        exclude = ('user',)
        read_only_fields = ('deleted', 'records')

    def validate_number(self, num):
        if len(num) == 15:
            arr = num.split('-')
            if len(arr) == 4:
                if len(arr[0]) == 3 and len(arr[1]) == len(arr[2]) == 4 and len(arr[3]) == 1:
                    if all([y.isdigit() for x in arr for y in x]):
                        return num
        raise ValidationError("Pattern of number is not valid")


class CowDetailSerializer(CowSerializer):
    records = RecordSerializer(many=True, read_only=True)

    class Meta:
        model = Cow
        exclude = ('user',)
