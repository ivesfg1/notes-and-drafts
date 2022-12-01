from django.urls import path, include

from . import views
from .api.routers import router

urlpatterns = [
    path("", views.group_list, name="group-list"),
    path("<uuid:pk>/", views.group_detail, name="group-detail"),
    path("<uuid:pk>/edit/", views.group_edit, name="group-edit"),
    path("<uuid:pk>/delete/", views.group_delete, name="group-delete"),
]

urlpatterns += [path("api/", include(router.urls))]
