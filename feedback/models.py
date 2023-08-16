from django.db import models
from user.models import Main_User
from products.models import Course, Track

class Feedback(models.Model):
    user = models.ForeignKey(Main_User, on_delete=models.SET_NULL, null=True, blank=True, related_name="user_feedbacks")
    rating = models.FloatField(max_length=50)
    review = models.TextField(max_length=250, blank=True, null=True)
    course = models.ForeignKey(
        "products.Course", on_delete=models.SET_NULL, null=True, blank=True)
    track = models.ForeignKey(
        "products.Track", on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.email}"
    


