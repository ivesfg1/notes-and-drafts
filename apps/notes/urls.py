from django.urls import path, include

from . import views
from .api.routers import router


# TODO: pensar em como vai ser a questao de editar anotação, pq eu nao quero
# que precise sair da pagina, quero deixar single page, talvez precise de JS

draft_urls = [
    path("", views.draft_list, name="draft-list"),
]

note_urls = [
    path("<uuid:pk>/delete/", views.note_delete, name="note-delete"),
]

app_urls = [
    path("drafts/", include(draft_urls)),
    path("notes/", include(note_urls)),
]

urlpatterns = [
    path("", include(app_urls)),
    path("api/", include(router.urls)),
]
