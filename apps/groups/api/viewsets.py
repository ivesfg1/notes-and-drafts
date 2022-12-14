from rest_framework import viewsets

from rest_framework.decorators import action

from .serializers import GroupSerializer
from ..models import Group

from apps.notes.api.serializers import NoteSerializer
from apps.notes.models import Note


# # Se for usar as rotas da Lib Nested Routers, basta essa ViewSet
# class GroupViewset(viewsets.ModelViewSet):

#     serializer_class = GroupSerializer

#     def get_queryset(self):
#         user = self.request.user
#         return Group.objects.filter(owner=user)


class GroupViewset(viewsets.ModelViewSet):

    serializer_class = GroupSerializer

    def get_queryset(self):

        user = self.request.user
        queryset = Group.objects.filter(owner=user)

        if "notes" in self.action:
            group_pk = self.kwargs["pk"]
            queryset = Note.objects.filter(group=group_pk, owner=user)

        return queryset

    def get_serializer_class(self):

        if "notes" in self.action:
            return NoteSerializer

        return super().get_serializer_class()

    def get_object(self):

        if "notes" in self.action:
            from rest_framework.generics import get_object_or_404

            queryset = self.filter_queryset(self.get_queryset())

            note_pk = self.kwargs["note_pk"]
            note = get_object_or_404(queryset, pk=note_pk)
            return note  # TODO: vai precisar personalizar o check_object_permissions tbm antes de retornar o note

        return super().get_object()

    def get_serializer_context(self):

        """
        Personalizei pra poder chamar o group_pk no .create() do serializer de
        NoteSerializer ao inves de passar diretamente pela @action de notes_create aqui

        referencias: https://stackoverflow.com/questions/32810354/django-1-8-getting-kwargs-in-serializer
        """

        context = super().get_serializer_context()

        if self.action in ["notes_create"]:
            context.update({"group_pk": self.kwargs["pk"]})

        return context

    @action(detail=True, methods=["get"])
    def notes(self, request, pk=None):
        return self.list(request)

    @notes.mapping.post
    def notes_create(self, request, pk=None):
        return self.create(request)

    @action(detail=True, methods=["get"], url_path=r"notes/(?P<note_pk>[^/.]+)")
    def notes_retrieve(self, request, pk=None, note_pk=None):
        return self.retrieve(request)

    @notes_retrieve.mapping.put
    def notes_update(self, request, pk=None, note_pk=None):
        return self.update(request)

    @notes_retrieve.mapping.patch
    def notes_partial_update(self, request, pk=None, note_pk=None):
        return self.partial_update(request)

    @notes_retrieve.mapping.delete
    def notes_delete(self, request, pk=None, note_pk=None):
        return self.destroy(request)
