from django import forms

from .models import Group, Note


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ("title", "description")


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ("body",)
