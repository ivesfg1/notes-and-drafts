from rest_framework.routers import DefaultRouter

from .viewsets import NoteViewset, GroupViewset

notes_and_groups_router = DefaultRouter()
notes_and_groups_router.register("notes", NoteViewset, basename="api-note")
notes_and_groups_router.register("groups", GroupViewset, basename="api-group")
