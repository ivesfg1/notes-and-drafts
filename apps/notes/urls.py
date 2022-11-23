from django.urls import path, include

from . import views

from .api.routers import notes_and_groups_router

# TODO: pensar em como vai ser a questao de editar anotação, pq eu nao quero
# que precise sair da pagina, quero deixar single page, talvez precise de JS

urlpatterns = [
    # drafts urls
    path("drafts/", views.draft_list, name="draft-list"),
    # notes urls
    path("notes/<uuid:pk>/delete/", views.note_delete, name="note-delete"),
    # groups urls
    path("groups/", views.group_list, name="group-list"),
    path("groups/<uuid:pk>/", views.group_detail, name="group-detail"),
    path("groups/<uuid:pk>/edit/", views.group_edit, name="group-edit"),
    path("groups/<uuid:pk>/delete/", views.group_delete, name="group-delete"),
    # api views
    path("api/", include(notes_and_groups_router.urls)),
]
