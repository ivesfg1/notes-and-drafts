from rest_framework import routers

from .viewsets import GroupViewset


router = routers.DefaultRouter()
router.register("groups", GroupViewset, basename="api-groups")
