from django.db import models
from django.conf import settings

from ..base_app.models import BaseModel

USER = settings.AUTH_USER_MODEL


class Group(BaseModel):
    title = models.CharField(max_length=255, verbose_name="Título")
    description = models.TextField(verbose_name="Descrição")
    owner = models.ForeignKey(
        USER,
        on_delete=models.CASCADE,
        related_name="note_groups",  # senao da conflito com o atributo "groups" que o proprio usuario do django ja tem
        related_query_name="note_group",
    )

    def get_notes(self):
        return self.notes.all()

    def __str__(self):
        return self.title


class NoteManager(models.Manager):
    def global_notes(self):
        """
        Returns a queryset containing all notes that aren't related to any group.
        These are the "Global" notes, or "drafts".

        I choose to do it that way so that i didn't have to create two different
        but instead very similar models.
        """
        queryset = self.get_queryset()
        return queryset.filter(group__isnull=True)  # same as .filter(group=None)


class Note(BaseModel):
    body = models.TextField()

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name="notes",
        related_query_name="note",
        null=True,
        blank=True,
    )
    owner = models.ForeignKey(
        USER,
        on_delete=models.CASCADE,
        related_name="notes",
        related_query_name="note",
    )

    def __str__(self):
        group_name = self.group or "Anotação Global"
        return f"{group_name}: {self.body[:30]}..."
