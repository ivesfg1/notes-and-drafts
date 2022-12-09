from rest_framework import viewsets, status

from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import GroupSerializer
from ..models import Group

from apps.notes.api.serializers import NoteSerializer
from apps.notes.models import Note


class GroupViewset(viewsets.ModelViewSet):

    serializer_class = GroupSerializer

    def get_queryset(self):
        user = self.request.user
        return Group.objects.filter(owner=user)

    @action(detail=True, methods=["get"])
    def notes(self, request, pk=None):

        group = self.get_object()
        queryset = group.get_notes()

        note_serializer = NoteSerializer(queryset, many=True)
        return Response(note_serializer.data)

    @notes.mapping.post
    def notes_create(self, request, pk=None):

        group = self.get_object()

        validated_data = request.data
        validated_data["owner"] = request.user.pk
        validated_data["group"] = group.pk

        note_serializer = NoteSerializer(data=validated_data)
        note_serializer.is_valid(raise_exception=True)
        note_serializer.save()

        headers = self.get_success_headers(note_serializer.data)

        return Response(
            note_serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    @action(detail=True, methods=["get"], url_path=r"notes/(?P<note_pk>[^/.]+)")
    def notes_retrieve(self, request, pk=None, note_pk=None):
        """
        Por padrao get_object() vai usar o "pk" a nao ser que eu sobreescreva o atributo lookup_field da classe
        e mesmo assim, o lookup_field é so pra eu dizer qual campo do model de Group usar pra pegar o obj
        entao nao pode ser algo do tipo "group_pk" por exemplo, pois tem que ser campo do model
        """

        group = self.get_object()
        queryset = group.get_notes()

        try:
            note = queryset.get(pk=note_pk)
        except Note.DoesNotExist:
            return Response({"detail": "Not found."}, status=404)

        serializer = NoteSerializer(note, many=False)
        return Response(serializer.data)

    @notes_retrieve.mapping.put  # TODO: Ver se tem como evitar esse codigo duplicado chamando a url de retrieve pelo reverse() (e em outros cantos tbm)
    def notes_update(self, request, pk=None, note_pk=None):

        group = self.get_object()
        queryset = group.get_notes()

        try:
            note = queryset.get(pk=note_pk)
        except Note.DoesNotExist:
            return Response({"detail": "Not found."}, status=404)

        validated_data = request.data
        validated_data["owner"] = request.user.pk
        validated_data["group"] = group.pk

        note_serializer = NoteSerializer(data=validated_data, instance=note)
        note_serializer.is_valid(raise_exception=True)
        note_serializer.save()

        headers = self.get_success_headers(note_serializer.data)

        return Response(
            note_serializer.data,
            status=status.HTTP_200_OK,
            headers=headers,
        )

    @notes_retrieve.mapping.patch  # TODO: Ver se tem como evitar esse codigo duplicado chamando a url de retrieve pelo reverse() (e em outros cantos tbm)
    def notes_partial_update(self, request, pk=None, note_pk=None):

        # TODO: Olhar tbm o update mixin pra melhorar essa questao do partial e pra entender melhor tbm

        group = self.get_object()
        queryset = group.get_notes()

        try:
            note = queryset.get(pk=note_pk)
        except Note.DoesNotExist:
            return Response({"detail": "Not found."}, status=404)

        validated_data = request.data

        note_serializer = NoteSerializer(
            data=validated_data, instance=note, partial=True
        )
        note_serializer.is_valid(raise_exception=True)
        note_serializer.save()

        headers = self.get_success_headers(note_serializer.data)

        return Response(
            note_serializer.data,
            status=status.HTTP_200_OK,
            headers=headers,
        )

    @notes_retrieve.mapping.delete  # TODO: Ver se tem como evitar esse codigo duplicado chamando a url de retrieve pelo reverse() (e em outros cantos tbm)
    def notes_partial_update(self, request, pk=None, note_pk=None):

        group = self.get_object()
        queryset = group.get_notes()

        try:
            note = queryset.get(pk=note_pk)
        except Note.DoesNotExist:
            return Response({"detail": "Not found."}, status=404)

        note.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
