from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import WeeklyReportViewSet, dashboard_summary

router = DefaultRouter()
router.register("", WeeklyReportViewSet, basename="report")

urlpatterns = [
    path("dashboard/summary/", dashboard_summary, name="dashboard-summary"),
] + router.urls
