from django.db import models
from user.models import User
from storages.backends.s3boto3 import S3Boto3Storage
import environ

env = environ.Env()
env.read_env()


class YourS3Storage(S3Boto3Storage):
    bucket_name = env("AWS_STORAGE_BUCKET_NAME")
    file_overwrite = False  # Optional: Set to True if you want to overwrite existing files


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
    # HTTP_CHOICES = [
    #     ('HTTP', 'HTTP'),
    #     ('HTTPS', 'HTTPS'),
    # ]
    APPLICATION_TYPE_CHOICES = [
        ('External', 'External'),
        ('Internal', 'Internal'),
    ]

    scan_type = models.CharField(max_length=100, choices=SCAN_TYPE_CHOICES,null=True,blank=True)
    scan_date = models.DateTimeField(null=True,blank=True)
    severity = models.CharField(max_length=100, choices=SEVERITY_CHOICES,null=True,blank=True)
    remediation = models.TextField(null=True,blank=True)
    assigned_to = models.ManyToManyField('Department', related_name="department_scans")
    scan_progress = models.CharField(max_length=100, choices=PROGRESS_CHOICES,null=True,blank=True)
    testing_method = models.CharField(max_length=100, choices=TESTING_METHOD_CHOICES,null=True,blank=True)
    target = models.CharField(max_length=100, choices=TARGET_CHOICES,null=True,blank=True)
    target_value = models.CharField(max_length=100, null=True, blank=True)
    application_type = models.CharField(max_length=100, choices=APPLICATION_TYPE_CHOICES,null=True,blank=True)
    file_upload = models.FileField(upload_to="security/file_uploads",null=True, blank=True)  # For general file uploads
    poc = models.FileField(upload_to='security/poc_uploads',null=True, blank=True)  # For image uploads (e.g., PoC photo)
    # created_at= models.DateTimeField(auto_now_add=True, null=True, blank=True)


    def __str__(self):
        return f"Scan {self.id}"
    
    class Meta:
        verbose_name_plural = "Scans"



class Department(models.Model):
    name = models.CharField(max_length=250, null=True,blank=True,unique=True)
    email = models.EmailField(null=True, blank=True, unique=True)

    def __str__(self):
        return f'{self.name}'



class Comment(models.Model):
    scan = models.ForeignKey(
        Scan, on_delete=models.CASCADE, related_name='comments')
    parent_comment = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    isPrimaryComment = models.BooleanField(default=False)
    isSecondaryComment = models.BooleanField(default=True)
    # department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True,blank=True)
    comment = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.department.email} - {self.scan.scan_type}'
        
    class Meta:
        verbose_name_plural = "Comments"



# class Reply(models.Model):
#     comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     content = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         verbose_name_plural = "Replies"
    