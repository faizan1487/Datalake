from django.db import models
from user.models import Main_User


class Feedback(models.Model):
    user = models.ForeignKey(Main_User, on_delete=models.SET_NULL, null=True, blank=True, related_name="user_feedbacks")
    rating = models.FloatField(max_length=50)
    review = models.TextField(max_length=250, blank=True, null=True)
    course = models.CharField(max_length=1000, null=True, blank=True)
    track = models.CharField(max_length=1000, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    working = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email}"