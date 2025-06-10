from django.db import models
from api.models.issue import Issue


class IssueAuditLog(models.Model):
    """
    Stores a historical record of actions taken on an issue for audit and traceability.
    """
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name="audit_logs")
    action_by = models.ForeignKey('api.UserData', on_delete=models.SET_NULL, null=True)
    field_changed = models.CharField(max_length=100)
    old_value = models.TextField(null=True, blank=True)
    new_value = models.TextField(null=True, blank=True)
    changed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.issue.title} - {self.field_changed}: {self.old_value} → {self.new_value}"
