from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers

from cowapp.models import Cow, Record


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'cows', 'records', 'auth_token')
        read_only_fields = ('cows', 'records', 'auth_token')

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
    cow_summary = serializers.ReadOnlyField(source='cow.summary')
    cow_number = serializers.ReadOnlyField(source='cow.number')

    class Meta:
        model = Record
        exclude = ('user',)

    def validate_cow(self, cow):
        if cow.user != self.context['request'].user:
            raise serializers.ValidationError('소유 중인 개체에 대해서만 이력을 등록할 수 있습니다.')
        return cow


class CowSerializer(serializers.ModelSerializer):
    sex = serializers.ChoiceField(choices=[('female', 'female'), ('male', 'male')])
    records = RecordSerializer(many=True, read_only=True)
    summary = serializers.ReadOnlyField()
    mother_id = serializers.SerializerMethodField()

    class Meta:
        model = Cow
        exclude = ('user',)

    def get_mother_id(self, instance):
        mother = Cow.objects.filter(user=instance.user, number=instance.mother_number).first()
        if mother:
            return mother.id
        return None

    def validate_number(self, num):
        if len(num) == 15:
            arr = num.split('-')
            if len(arr) == 4:
                if len(arr[0]) == 3 and len(arr[1]) == len(arr[2]) == 4 and len(arr[3]) == 1:
                    if all([y.isdigit() for x in arr for y in x]):
                        return num
        raise serializers.ValidationError("개체번호의 패턴이 유효하지 않습니다.")

    def validate_mother_number(self, num):
        if not num:
            return num
        return self.validate_number(num)
