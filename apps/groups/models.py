from django.db import models
from django.conf import settings

from apps.base_app.models import BaseModel

USER_MODEL_STRING = settings.AUTH_USER_MODEL


class Group(BaseModel):
    title = models.CharField(max_length=255, verbose_name="Título")
    description = models.TextField(verbose_name="Descrição")
    owner = models.ForeignKey(
        USER_MODEL_STRING,
        on_delete=models.CASCADE,
        related_name="note_groups",  # senao da conflito com o atributo "groups" que o proprio usuario do django ja tem
        related_query_name="note_group",
    )

    def get_notes(self):
        return self.notes.all()

    def __str__(self):
        return self.title
