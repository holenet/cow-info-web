from rest_framework import serializers

from cowapp.models import Cow, Record


def cow_number_restriction(num):
    if len(num)==15:
        arr = num.split('-')
        if len(arr)==4:
            if len(arr[0])==3 and len(arr[1])==len(arr[2])==4 and len(arr[3])==1:
                if all([y.isdigit() for x in arr for y in x]):
                    return num
    raise serializers.ValidationError("pattern is not valid")


class CowField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        return Cow.objects.filter(user=self.context['request'].user)


class RecordSerializer(serializers.ModelSerializer):
    cow = CowField()

    class Meta:
        model = Record
        exclude = ('user',)


class CowSerializer(serializers.ModelSerializer):
    number = serializers.CharField(validators=[cow_number_restriction])
    sex = serializers.ChoiceField(choices=[('female', 'female'), ('male', 'male')])

    class Meta:
        model = Cow
        exclude = ('user',)


class CowDetailSerializer(CowSerializer):
    records = RecordSerializer(many=True, read_only=True)

    class Meta:
        model = Cow
        exclude = ('user',)
