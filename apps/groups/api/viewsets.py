from rest_framework import viewsets

from .serializers import GroupSerializer
from ..models import Group


class GroupViewset(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

