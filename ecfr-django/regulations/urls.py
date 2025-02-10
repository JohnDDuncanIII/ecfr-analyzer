from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()
router.register(r"agency", views.AgencyResource, basename="agency")
router.register(r"agency-name", views.AgencyNameResource, basename="agency-name")
router.register(r"title", views.TitleResource, basename="title")

urlpatterns = [
    path("api/", include(router.urls)),
]
