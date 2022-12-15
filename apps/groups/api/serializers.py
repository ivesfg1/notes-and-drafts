from rest_framework import serializers

from ..models import Group


class GroupSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Group
        fields = (
            "id",
            "title",
            "description",
            "created_at",
            "last_updated",
            "owner",
        )
