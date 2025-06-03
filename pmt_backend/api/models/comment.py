from django.db import models
from django.contrib.auth import get_user_model
from api.models.issue import Issue

User = get_user_model()


class Comment(models.Model):
    """
    Represents a comment made by a user on a specific issue.
    """
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.author.username} on {self.issue.title}"
