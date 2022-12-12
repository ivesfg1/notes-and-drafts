from rest_framework import serializers

from ..models import Note

from apps.groups.models import Group


# class NoteSerializer(serializers.ModelSerializer):
#     owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

#     class Meta:
#         model = Note
#         fields = "__all__"


class NoteSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Note
        fields = "__all__"

    def create(self, validated_data):
        """
        Codigo abaixo é possivel pois na Viewset de Group que usa esse Serializer
        eu personalizei o get_serializer_context para a ação de Create, ver codigo la
        aí agora tenho um campo extra no context, que é o pk do Group
        """
        group_pk = self.context["group_pk"]
        validated_data["group"] = Group.objects.get(pk=group_pk)
        return super().create(validated_data)


class DraftSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Note
        exclude = ["group"]
