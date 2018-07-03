from django.contrib.auth.models import User
from django.core.exceptions import FieldError, ValidationError
from django.db import IntegrityError
from rest_framework import generics, exceptions
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED

from cowapp.models import Cow, Record
from cowapp.permissions import IsOwner
from cowapp.serializers import CowSerializer, RecordSerializer, UserSerializer


class FilterOrderAPIView(generics.GenericAPIView):
    """
    Custom supporting APIView for filtering and ordering queryset based on query_params.

    By extending this class, the APIView will automatically filter and order queryset
    if the request has query_params.
    Keys of the query_params that is not valid for the function 'QuerySet.filter', except 'order_by', would be ignored.
    The value of the key 'order_by' that is not valid for the function 'QuerySet.order_by' would be ignored.
    """

    def filter_queryset(self, queryset):
        ordering = None
        options = {}
        for key, value in self.request.query_params.items():
            if key == 'order_by' and value:
                try:
                    queryset.filter(**{value[value[0]=='-':]+'__isnull': 'True'})
                    ordering = value
                except (FieldError, ValueError, ValidationError):
                    pass
                continue
            try:
                queryset.filter(**{key: value})
                options.update({key: value})
            except (FieldError, ValueError, ValidationError):
                pass
        if ordering:
            return queryset.filter(**options).order_by(ordering)
        return queryset.filter(**options)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)


class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return User.objects.get_by_natural_key(self.request.user.username)


class CowList(FilterOrderAPIView, generics.ListCreateAPIView):
    queryset = Cow.objects.all()
    serializer_class = CowSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
        except IntegrityError:
            raise exceptions.ValidationError(dict(number='이 번호를 가진 개체가 이미 있습니다.'))
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CowDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cow.objects.all()
    serializer_class = CowSerializer
    permission_classes = (IsAuthenticated, IsOwner)


class RecordList(FilterOrderAPIView, generics.ListCreateAPIView):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RecordDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer
    permission_classes = (IsAuthenticated, IsOwner)
