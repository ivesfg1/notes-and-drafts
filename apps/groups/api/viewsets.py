from rest_framework import viewsets, status

from rest_framework.decorators import action
from rest_framework.response import Response

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


class ExtraSerializerClassMixin:
    """
    Mixin para utilização de duas classes de serializers em uma mesma Viewset.

    Foi necessário para o caso de GroupViewset, que possui @actions para realizar
    ações com serializers e objetos de Note, porem todos os metodos padroes pegavam
    serializers e objetos de Group
    """

    extra_serializer_class = None

    def get_extra_serializer(self, *args, **kwargs):

        extra_serializer_class = self.get_extra_serializer_class()
        kwargs.setdefault("context", self.get_serializer_context())
        return extra_serializer_class(*args, **kwargs)

    def get_extra_serializer_class(self):

        assert self.extra_serializer_class is not None, (
            "Due to the ExtraSerializerClassMixin being used, '%s' should either include a `extra_serializer_class` attribute, "
            "or override the `get_extra_serializer_class()` method."
            % self.__class__.__name__
        )
        return self.extra_serializer_class


class GroupViewset(ExtraSerializerClassMixin, viewsets.ModelViewSet):

    serializer_class = GroupSerializer
    extra_serializer_class = NoteSerializer

    def get_queryset(self):
        user = self.request.user
        return Group.objects.filter(owner=user)

    @action(detail=True, methods=["get"])
    def notes(self, request, pk=None):

        group = self.get_object()
        queryset = group.get_notes()

        note_serializer = self.get_extra_serializer(queryset, many=True)
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
