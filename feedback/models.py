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
    
 

class FeedbackQuestion(models.Model):
    chapter_name = models.CharField(max_length=255,null=True)
    course_name = models.CharField(max_length=255,null=True)
    question_answer = models.JSONField()

    def __str__(self):
        return self.chapter_name or "-"



class FeedbackAnswers(models.Model):
    user_email = models.CharField(max_length=255)
    question_answer = models.JSONField()
    created_at = models.DateTimeField(null=True,blank=True)
    feedback_question_id = models.ForeignKey(FeedbackQuestion, on_delete=models.CASCADE, null=True)

    def course_name(self):
        if self.feedback_question_id.course_name:
            return self.feedback_question_id.course_name
    
    def chapter_name(self):
        if self.feedback_question_id.chapter_name:
            return self.feedback_question_id.chapter_name
    def __str__(self):
        if self.user_email:
            return self.user_email


