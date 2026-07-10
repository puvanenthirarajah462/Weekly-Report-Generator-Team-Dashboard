from datetime import timedelta

from django.db.models import Count, Q
from django.utils import timezone
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from accounts.models import User
from accounts.permissions import IsManager
from .models import WeeklyReport
from .serializers import WeeklyReportSerializer


class WeeklyReportViewSet(viewsets.ModelViewSet):
    """
    Team members: only see/manage their own reports.
    Managers: can see everyone's reports, filterable via query params:
      ?user=<id>&project=<id>&week=<YYYY-MM-DD>&start=<YYYY-MM-DD>&end=<YYYY-MM-DD>
    """

    serializer_class = WeeklyReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = WeeklyReport.objects.select_related("user", "project")

        if not user.is_manager:
            return qs.filter(user=user)

        params = self.request.query_params
        if params.get("user"):
            qs = qs.filter(user_id=params["user"])
        if params.get("project"):
            qs = qs.filter(project_id=params["project"])
        if params.get("week"):
            qs = qs.filter(week_start=params["week"])
        if params.get("start"):
            qs = qs.filter(week_start__gte=params["start"])
        if params.get("end"):
            qs = qs.filter(week_start__lte=params["end"])
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated, IsManager])
def dashboard_summary(request):
    """
    Aggregated metrics + chart data for the manager dashboard.
    Optional query param: ?week=<YYYY-MM-DD> (Monday). Defaults to the current week.
    """
    week_param = request.query_params.get("week")
    if week_param:
        week_start = week_param
    else:
        today = timezone.localdate()
        week_start = today - timedelta(days=today.weekday())

    all_users = User.objects.filter(role=User.Role.TEAM_MEMBER)
    week_reports = WeeklyReport.objects.filter(week_start=week_start)

    total_expected = all_users.count()
    total_submitted = week_reports.filter(status=WeeklyReport.Status.SUBMITTED).count()
    compliance_rate = round((total_submitted / total_expected) * 100, 1) if total_expected else 0

    open_blockers = week_reports.exclude(blockers="").exclude(blockers__isnull=True).count()

    # Submission status per team member for the selected week
    status_by_member = []
    for u in all_users:
        r = week_reports.filter(user=u).first()
        if r and r.status == WeeklyReport.Status.SUBMITTED:
            member_status = "submitted"
        elif r:
            member_status = "pending"
        else:
            member_status = "pending"
        status_by_member.append({"user": u.username, "status": member_status})

    # Tasks/reports trend over the last 8 weeks (team-wide)
    trend = []
    today = timezone.localdate()
    current_monday = today - timedelta(days=today.weekday())
    for i in range(7, -1, -1):
        wk = current_monday - timedelta(weeks=i)
        count = WeeklyReport.objects.filter(
            week_start=wk, status=WeeklyReport.Status.SUBMITTED
        ).count()
        trend.append({"week": str(wk), "reports_submitted": count})

    # Workload distribution by project (submitted reports, all-time, top 10)
    workload = (
        WeeklyReport.objects.filter(status=WeeklyReport.Status.SUBMITTED)
        .values("project__name")
        .annotate(count=Count("id"))
        .order_by("-count")[:10]
    )
    workload_data = [{"project": w["project__name"] or "Unassigned", "count": w["count"]} for w in workload]

    recent_activity = (
        WeeklyReport.objects.filter(status=WeeklyReport.Status.SUBMITTED)
        .select_related("user", "project")
        .order_by("-submitted_at")[:10]
    )
    recent = [
        {
            "user": r.user.username,
            "project": r.project.name if r.project else None,
            "week_start": str(r.week_start),
            "submitted_at": r.submitted_at,
        }
        for r in recent_activity
    ]

    return Response(
        {
            "week_start": str(week_start),
            "summary": {
                "total_submitted": total_submitted,
                "total_expected": total_expected,
                "compliance_rate": compliance_rate,
                "open_blockers": open_blockers,
            },
            "status_by_member": status_by_member,
            "trend": trend,
            "workload_by_project": workload_data,
            "recent_activity": recent,
        }
    )
