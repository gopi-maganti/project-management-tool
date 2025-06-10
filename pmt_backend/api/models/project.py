from django.db import models
from api.constants.constants import ROLE_CHOICES


class Project(models.Model):
    """
    Represents a project in the system. Each project can have multiple members and issues.
    """
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey('api.UserData', on_delete=models.CASCADE, related_name="created_projects")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name


class ProjectMember(models.Model):
    """
    Represents a user associated with a project along with their role (e.g., admin, developer).
    """
    user = models.ForeignKey('api.UserData', on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="members")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    class Meta:
        unique_together = ("user", "project")
        verbose_name = "Project Member"
        verbose_name_plural = "Project Members"

    def __str__(self) -> str:
        return f"{self.user.username} - {self.project.name} ({self.role})"
