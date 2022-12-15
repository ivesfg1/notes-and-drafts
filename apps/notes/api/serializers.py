from rest_framework import serializers

from ..models import Note

from apps.groups.models import Group


class DraftSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Note
        fields = (
            "id",
            "body",
            "created_at",
            "last_updated",
            "owner",
        )


class NoteSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Note
        fields = (
            "id",
            "body",
            "group",
            "created_at",
            "last_updated",
            "owner",
        )

    def create(self, validated_data):
        group_pk = self.context["group_pk"]
        validated_data["group"] = Group.objects.get(pk=group_pk)
        return super().create(validated_data)
