from django.db import models

from ..base_app.models import BaseModel


class Group(BaseModel):
    title = models.CharField(max_length=255, verbose_name="Título")
    description = models.TextField(verbose_name="Descrição")

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


# TODO: ver como vai ficar a questao de imagens e videos pq eu vou querer poder colocar legenda ou nao
# entao acho que vai ter que ser um model so pra o video e um many to many aqui na note, mesmo pra imagens
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

    def __str__(self):
        group_name = self.group or "Anotação Global"
        return f"{group_name}: {self.body[:30]}..."
