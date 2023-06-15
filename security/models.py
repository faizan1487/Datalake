from django.db import models
from user.models import User


class Scan(models.Model):
    SCAN_TYPE_CHOICES = [
        ('Application', 'Application'),
        ('Server', 'Server'),
        ('Database', 'Database'),
        ('Other', 'Other'),
    ]
    SEVERITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]
    PROGRESS_CHOICES = [
        ('Not Started', 'Not Started'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]
    TESTING_METHOD_CHOICES = [
        ('Auto', 'Auto'),
        ('Manual', 'Manual'),
        ('Auto&Manual', 'Auto&Manual'),
    ]
    TARGET_CHOICES = [
        ('IP', 'IP'),
        ('Domain', 'Domain'),
        ('CIDR', 'CIDR'),
    ]
    HTTP_CHOICES = [
        ('HTTP', 'HTTP'),
        ('HTTPS', 'HTTPS'),
    ]
    APPLICATION_TYPE_CHOICES = [
        ('External', 'External'),
        ('Internal', 'Internal'),
    ]

    scan_type = models.CharField(max_length=100, choices=SCAN_TYPE_CHOICES)
    scan_date = models.DateTimeField(auto_now_add=True)
    severity = models.CharField(max_length=100, choices=SEVERITY_CHOICES)
    remediation = models.TextField()
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="user_scans")
    scan_progress = models.CharField(max_length=100, choices=PROGRESS_CHOICES)
    testing_method = models.CharField(max_length=100, choices=TESTING_METHOD_CHOICES)
    target = models.CharField(max_length=100, choices=TARGET_CHOICES)
    http_or_https = models.CharField(max_length=100, choices=HTTP_CHOICES)
    application_type = models.CharField(max_length=100, choices=APPLICATION_TYPE_CHOICES)
    findings_and_recommendations = models.TextField()
    file_upload = models.FileField(upload_to="media/security/file_uploads",null=True, blank=True)  # For general file uploads
    poc = models.ImageField(upload_to='media/securitypoc_uploads/',null=True, blank=True)  # For image uploads (e.g., PoC photo)

    def __str__(self):
        return f"Scan {self.id}"

# class TeamMember(models.Model):
#     name = models.CharField(max_length=100)

#     def __str__(self):
#         return self.name
