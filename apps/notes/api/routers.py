from rest_framework import routers

from .viewsets import DraftViewset


router = routers.DefaultRouter()
router.register("drafts", DraftViewset, basename="api-drafts")
