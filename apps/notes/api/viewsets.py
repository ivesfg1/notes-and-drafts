from rest_framework import viewsets

from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import NoteSerializer
from ..models import Note


class NoteViewset(viewsets.ModelViewSet):

    serializer_class = NoteSerializer

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(owner=user)

    @action(detail=False, methods=["get"])
    def drafts(self, request):
        user = request.user

        queryset = Note.objects.global_notes().filter(owner=user)
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)
