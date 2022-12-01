from rest_framework import viewsets

from .serializers import NoteSerializer
from ..models import Note


class NoteViewset(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

