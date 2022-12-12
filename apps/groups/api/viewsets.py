from rest_framework import viewsets, status

from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import GroupSerializer
from ..models import Group

from apps.notes.api.serializers import NoteSerializer
from apps.notes.models import Note


class GroupViewset(viewsets.ModelViewSet):

    # class SERIALIZER_CLASSES:

    serializer_class = GroupSerializer

    def get_queryset(self):
        user = self.request.user
        return Group.objects.filter(owner=user)

    def get_serializer_class(self, notes=False):
        """
        Adicionei validação pra puxar o serializer de Note, para isso também tive
        que personalizar o metodo get_serializer() para poder receber o parametro "notes"
        """
        if notes:
            return NoteSerializer

        return super().get_serializer_class()

    def get_serializer(self, *args, notes=False, **kwargs):
        """
        Codigo copiado do codigo padrao: super().get_serializer() (padrao do DRF)
        Geralmente apenas o get_serializer_class é personalizavel, mas tive que
        personalizar esse também pra poder passar um valor adicional pra o metodo
        get_serializer_class para só então conseguir personalizar da maneira que
        queria.

        Ler mais sobre o que foi personalizado na funcao get_serializer_class().
        """
        serializer_class = self.get_serializer_class(notes)
        kwargs.setdefault("context", self.get_serializer_context())
        return serializer_class(*args, **kwargs)

    @action(detail=True, methods=["get"])
    def notes(self, request, pk=None):

        # queryset = self.filter_queryset(self.get_queryset())

        # page = self.paginate_queryset(queryset)
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True)
        #     return self.get_paginated_response(serializer.data)

        # serializer = self.get_serializer(queryset, many=True)
        # return Response(serializer.data)

        group = self.get_object()
        queryset = group.get_notes()

        # note_serializer = NoteSerializer(queryset, many=True)
        note_serializer = self.get_serializer(queryset, many=True, notes=True)

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

    # esse TODO ai debaixo talvez seja meio traiçoeiro por causa das permissoes, enfim é so olhar o get_object() original que vai dar pra entender
    @notes_retrieve.mapping.put  # TODO: ver uma maneira melhor ao inves chamar o self.notes_retrieve e personalizar tbm o get_object() pra poder usar com objetos de Note tbm
    def notes_update(self, request, pk=None, note_pk=None):

        note_retrieve = self.notes_retrieve(request, pk, note_pk)
        if note_retrieve.status_code == status.HTTP_404_NOT_FOUND:
            return note_retrieve

        group = self.get_object()
        queryset = group.get_notes()
        note = queryset.get(pk=note_pk)

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

    @notes_retrieve.mapping.patch  # TODO: ver uma maneira melhor ao inves chamar o self.notes_retrieve e personalizar tbm o get_object() pra poder usar com objetos de Note tbm
    def notes_partial_update(self, request, pk=None, note_pk=None):

        # TODO: Olhar tbm o update mixin pra melhorar essa questao do partial e pra entender melhor tbm

        note_retrieve = self.notes_retrieve(request, pk, note_pk)
        if note_retrieve.status_code == status.HTTP_404_NOT_FOUND:
            return note_retrieve

        group = self.get_object()
        queryset = group.get_notes()
        note = queryset.get(pk=note_pk)

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

    @notes_retrieve.mapping.delete  # TODO: ver uma maneira melhor ao inves chamar o self.notes_retrieve e personalizar tbm o get_object() pra poder usar com objetos de Note tbm
    def notes_delete(self, request, pk=None, note_pk=None):

        note_retrieve = self.notes_retrieve(request, pk, note_pk)
        if note_retrieve.status_code == status.HTTP_404_NOT_FOUND:
            return note_retrieve

        group = self.get_object()
        queryset = group.get_notes()
        note = queryset.get(pk=note_pk)

        note.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
