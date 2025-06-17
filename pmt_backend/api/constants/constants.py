"""
Constants required for the PMT Backend API
"""

# List of choices for the `login_type` field in the `LoginTypeSerializer`
# LOGIN_TYPE_CHOICES = (
#     ("username_password", "Username & Password"),
#     ("token", "Token"),
#     ("google", "Google SSO"),
#     ("facebook", "Facebook SSO"),
# )

# List of choices for the `role` field in the `ProjectMember` model
ROLE_CHOICES = (
    ("admin", "Admin"),
    ("manager", "Manager"),
    ("developer", "Developer"),
)

# List of choices for the `type` field in the `Issue` model
ISSUE_TYPES = (
    ("task", "Task"),
    ("bug", "Bug"),
    ("story", "Story"),
)

# List of choices for the `status` field in the `Issue` model
STATUS_CHOICES = (
    ("todo", "To Do"),
    ("in_progress", "In Progress"),
    ("done", "Done"),
    ("blocked", "Blocked"),
)

# List of choices for the `priority` field in the `Issue` model
PRIORITY_CHOICES = (
    ("low", "Low"),
    ("medium", "Medium"),
    ("high", "High"),
    ("critical", "Critical"),
)
