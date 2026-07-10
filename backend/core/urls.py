from django.contrib import admin
from django.http import JsonResponse
from django.urls import path, include


def api_root(request):
    return JsonResponse({
        "message": "Weekly Report Dashboard API",
        "status": "ok",
    })


urlpatterns = [
    path("", api_root, name="api-root"),
    path("admin/", admin.site.urls),
    path("api/auth/", include("accounts.urls")),
    path("api/projects/", include("projects.urls")),
    path("api/reports/", include("reports.urls")),
    path("api/ai/", include("aiassistant.urls")),
]
