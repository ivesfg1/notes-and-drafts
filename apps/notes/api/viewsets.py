from rest_framework import viewsets

from .serializers import DraftSerializer

from ..models import Note


class DraftViewset(viewsets.ModelViewSet):

    serializer_class = DraftSerializer

    def get_queryset(self):
        user = self.request.user
        return Note.objects.drafts().filter(owner=user)
