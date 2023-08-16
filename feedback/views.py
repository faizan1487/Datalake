from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
# Create your views here.
from .models import Feedback, FeedbackAnswers
from django.db.models import Q
from django.db.models import Count
from rest_framework import status
from django.http import HttpResponse
from threading import Thread
from datetime import date, datetime, timedelta
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class GetFeedbacks(APIView):
    def get(self, request):
        # q = self.request.GET.get('q', None) or None
        start_date = self.request.GET.get('start_date', None) or None
        end_date = self.request.GET.get('end_date', None) or None
        email = self.request.GET.get('email', None) or None
        track = self.request.GET.get('track', None) or None
        feedbacks = Feedback.objects.all().values("user__email","rating","review","course","track__name","created_at")

        if email:
            feedbacks = feedbacks.filter(user__email=email)
        
        if track:
            feedbacks = feedbacks.filter(track__name=track)

        return Response(feedbacks)
    

class GetFeedbackAnswers(APIView):
    def get(self, request):
        # q = self.request.GET.get('q', None) or None
        start_date = self.request.GET.get('start_date', None) or None
        end_date = self.request.GET.get('end_date', None) or None
        email = self.request.GET.get('email', None) or None
        track = self.request.GET.get('track', None) or None
        feedbacks = FeedbackAnswers.objects.all().values("user_email","feedback_question_id__course_name","question_answer","created_at")

        if email:
            feedbacks = feedbacks.filter(user_email=email)        
        if track:
            feedbacks = feedbacks.filter(track__name=track)

        return Response(feedbacks)