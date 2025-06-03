from django.db import models
from django.contrib.auth import get_user_model

from api.models.project import Project
from api.constants.constants import ISSUE_TYPES, STATUS_CHOICES, PRIORITY_CHOICES

User = get_user_model()


class Issue(models.Model):
    """
    Represents an issue (task, bug, or story) within a project.
    Each issue has a status, type, priority, and can be assigned to a user.
    """
    title: str = models.CharField(max_length=255)
    description: str = models.TextField(blank=True)

    type: str = models.CharField(max_length=20, choices=ISSUE_TYPES)
    status: str = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    priority: str = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    project: Project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='issues'
    )
    assignee = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_issues'
    )
    reporter = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reported_issues'
    )

    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"[{self.get_type_display()}] {self.title}"
