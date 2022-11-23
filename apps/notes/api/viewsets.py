from rest_framework import viewsets

from .serializers import NoteSerializer, GroupSerializer
from ..models import Note, Group


class NoteViewset(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer


class GroupViewset(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
