from django.db import models
from django.conf import settings

from apps.base_app.models import BaseModel
from apps.groups.models import Group

USER = settings.AUTH_USER_MODEL


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

    # manager

    objects = NoteManager()

    # fields

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
