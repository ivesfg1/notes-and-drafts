from rest_framework import viewsets

from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import NoteSerializer, DraftSerializer
from ..models import Note


class NoteViewset(viewsets.ModelViewSet):

    draft_actions = ["drafts", "drafts_create"]
    serializer_class = NoteSerializer

    def get_queryset(self):

        user = self.request.user
        queryset = Note.objects.all()

        if self.action in self.draft_actions:
            queryset = Note.objects.global_notes()

        return queryset.filter(owner=user)

    def get_serializer_class(self):
        if self.action in self.draft_actions:
            return DraftSerializer
        return super().get_serializer_class()

    @action(detail=False, methods=["get"])
    def drafts(self, request):
        return self.list(request)

    @drafts.mapping.post
    def drafts_create(self, request):
        return self.create(request)

    # @drafts.mapping
