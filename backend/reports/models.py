from django.conf import settings
from django.db import models
from projects.models import Project


class WeeklyReport(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        SUBMITTED = "submitted", "Submitted"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reports"
    )
    project = models.ForeignKey(
        Project, on_delete=models.SET_NULL, null=True, blank=True, related_name="reports"
    )
    # Monday of the reporting week — every report is anchored to a fixed week start
    # so reports are comparable across the team regardless of when they were filled in.
    week_start = models.DateField()

    tasks_completed = models.TextField(blank=True)
    tasks_planned = models.TextField(blank=True)
    blockers = models.TextField(blank=True)
    hours_worked = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    notes = models.TextField(blank=True)

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    submitted_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-week_start"]
        unique_together = ("user", "week_start")

    def __str__(self):
        return f"{self.user.username} - {self.week_start} ({self.status})"

    @property
    def has_open_blocker(self):
        return bool(self.blockers and self.blockers.strip())
