from rest_framework import routers

from .viewsets import NoteViewset


router = routers.DefaultRouter()
router.register("notes", NoteViewset, basename="api-notes")
