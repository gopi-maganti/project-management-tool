from django.db import models
from api.models.project import Project
from api.constants.constants import ISSUE_TYPES, STATUS_CHOICES, PRIORITY_CHOICES


class Issue(models.Model):
    """
    Represents an issue (task, bug, or story) within a project.
    Each issue has a status, type, priority, and can be assigned to a user.
    """
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    type = models.CharField(max_length=20, choices=ISSUE_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='issues')
    assignee = models.ForeignKey('api.UserData', on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_issues')
    reporter = models.ForeignKey('api.UserData', on_delete=models.SET_NULL, null=True, blank=True, related_name='reported_issues')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"[{self.get_type_display()}] {self.title}"
