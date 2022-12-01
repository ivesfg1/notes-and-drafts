from django.urls import path, include

from . import views
from .api.routers import router


# TODO: pensar em como vai ser a questao de editar anotação, pq eu nao quero
# que precise sair da pagina, quero deixar single page, talvez precise de JS

urlpatterns = [
    # drafts urls
    path("drafts/", views.draft_list, name="draft-list"),
    # notes urls
    path("notes/<uuid:pk>/delete/", views.note_delete, name="note-delete"),
]

urlpatterns += [path("api/", include(router.urls))]
