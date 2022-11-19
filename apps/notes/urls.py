from django.urls import path

from . import views

urlpatterns = [
    path("drafts/", views.draft_list, name="draft-list"),
    path("groups/", views.group_list, name="group-list"),
    path("groups/<uuid:pk>/", views.group_detail, name="group-detail"),
]
