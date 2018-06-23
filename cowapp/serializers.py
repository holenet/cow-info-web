from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers

from cowapp.models import Cow, Record


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'cows', 'records')
        read_only_fields = ('cows', 'records')

    def validate(self, data):
        if 'password' not in data:
            return data
        try:
            user = User(username=data['username']) if 'username' in data else self.instance
            validate_password(data['password'], user=user)
        except ValidationError as e:
            raise serializers.ValidationError(dict(password=e.messages))
        data['password'] = make_password(data['password'])
        return data


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

    def validate_number(self, num):
        if len(num) == 15:
            arr = num.split('-')
            if len(arr) == 4:
                if len(arr[0]) == 3 and len(arr[1]) == len(arr[2]) == 4 and len(arr[3]) == 1:
                    if all([y.isdigit() for x in arr for y in x]):
                        return num
        raise serializers.ValidationError("개체번호의 패턴이 유효하지 않습니다.")


class CowDetailSerializer(CowSerializer):
    records = RecordSerializer(many=True, read_only=True)

    class Meta:
        model = Cow
        exclude = ('user',)
