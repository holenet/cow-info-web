from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from cowapp.models import Cow
from cowapp.permissions import IsUser
from cowapp.serializers import CowSerializer, CowDetailSerializer


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
    permission_classes = (IsAuthenticated, IsUser)
