from django.core.exceptions import FieldError
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from cowapp.models import Cow, Record
from cowapp.permissions import IsOwner
from cowapp.serializers import CowSerializer, CowDetailSerializer, RecordSerializer


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
                except (FieldError, ValueError):
                    pass
                continue
            try:
                queryset.filter(**{key: value})
                options.update({key: value})
            except (FieldError, ValueError):
                pass
        if ordering:
            return queryset.filter(**options).order_by(ordering)
        return queryset.filter(**options)


class CowList(FilterOrderAPIView, generics.ListCreateAPIView):
    queryset = Cow.objects.all()
    serializer_class = CowSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CowDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cow.objects.all()
    serializer_class = CowDetailSerializer
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
