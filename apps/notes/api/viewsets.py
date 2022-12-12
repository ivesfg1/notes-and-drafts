from rest_framework import viewsets

from .serializers import DraftSerializer
from .serializers import NoteSerializer

from ..models import Note


class DraftViewset(viewsets.ModelViewSet):

    serializer_class = DraftSerializer

    def get_queryset(self):
        user = self.request.user
        return Note.objects.drafts().filter(owner=user)


class NoteViewset(viewsets.ModelViewSet):

    serializer_class = NoteSerializer

    def get_queryset(self):
        """
        referencia: https://github.com/alanjds/drf-nested-routers
        so funciona por causa da lib, a router ta definida em:
        groups.api.routers. com nome de: "nested_groups_notes_router
        """
        user = self.request.user
        return Note.objects.filter(owner=user, group=self.kwargs["group_pk"])
