from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from cowapp.models import Cow, Record
from cowapp.permissions import IsOwner
from cowapp.serializers import CowSerializer, CowDetailSerializer, RecordSerializer


class CowList(generics.ListCreateAPIView):
    serializer_class = CowSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Cow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CowDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cow.objects.all()
    serializer_class = CowDetailSerializer
    permission_classes = (IsAuthenticated, IsOwner)


class RecordList(generics.ListCreateAPIView):
    serializer_class = RecordSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if 'pk' in self.kwargs:
            return Record.objects.filter(cow_id=self.kwargs['pk'])
        return Record.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RecordDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RecordSerializer
    permission_classes = (IsAuthenticated, IsOwner)

    def get_queryset(self):
        return Record.objects.filter(user=self.request.user)
