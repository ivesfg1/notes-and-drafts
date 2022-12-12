from rest_framework import routers

from rest_framework_nested import routers as nested_routers

from .viewsets import GroupViewset

from apps.notes.api.viewsets import NoteViewset


router = routers.DefaultRouter()
router.register("groups", GroupViewset, basename="api-groups")

nested_router = nested_routers.NestedDefaultRouter(router, r"groups", lookup="group")
nested_router.register(r"notes", NoteViewset, basename="group-notes")
