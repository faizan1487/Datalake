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
from .models import FeedbackQuestion
from collections import defaultdict

# Create your views here.
class GetFeedbacks(APIView):
    def get(self, request):
        # q = self.request.GET.get('q', None) or None
        start_date = self.request.GET.get('start_date', None) or None
        end_date = self.request.GET.get('end_date', None) or None
        email = self.request.GET.get('email', None) or None
        track = self.request.GET.get('track', None) or None
        feedbacks = Feedback.objects.all().values("user__email","rating","review","course__name","track__name","created_at")
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
        course = self.request.GET.get('course', None) or None
        chapter = self.request.GET.get('chapter', None) or None
        feedbacks = FeedbackAnswers.objects.all().values("user_email","feedback_question_id__course_name","feedback_question_id__chapter_name","question_answer","created_at")

        if email:
            feedbacks = feedbacks.filter(user_email=email)        
        if course:
            feedbacks = feedbacks.filter(feedback_question_id__course_name=course)
        if chapter:
            feedbacks = feedbacks.filter(feedback_question_id__chapter_name=chapter)

        return Response(feedbacks)


class GetCoursesNames(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        queryset = FeedbackQuestion.objects.values('course_name').distinct()
        course_list = [item['course_name'] for item in queryset]
        return Response(course_list)
    

class GetCoursesChapters(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        queryset = FeedbackQuestion.objects.values('course_name','chapter_name')
        print(queryset)

        for i in queryset:
            pass
        course_list = [item['course_name'] for item in queryset]
        return Response(course_list)
    
        # Create a defaultdict to group chapter names by course names
        grouped_data = defaultdict(list)


