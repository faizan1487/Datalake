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
    permission_classes = [IsAuthenticated]
    def get(self, request):
        # q = self.request.GET.get('q', None) or None
        start_date = self.request.GET.get('start_date', None) or None
        end_date = self.request.GET.get('end_date', None) or None
        email = self.request.GET.get('email', None) or None
        track = self.request.GET.get('track', None) or None
        feedbacks = Feedback.objects.all().values("user__email","rating","review","course__name","track__name","created_at")
        if email:
            feedbacks = feedbacks.filter(user__email=email)


        # Extract the 'created_at' values
        created_at_values = [item['created_at'] for item in feedbacks]

        # Find the minimum and maximum 'created_at' valus    
        if not start_date:
            start_date = min(created_at_values)
        if not end_date:
            end_date = max(created_at_values)
            
        if track:
            feedbacks = feedbacks.filter(track__name=track)

        feedbacks = feedbacks.filter(Q(created_at__date__lte=end_date) & Q(created_at__date__gte=start_date))

        return Response(feedbacks)
    

class GetFeedbackAnswers(APIView):
    permission_classes = [IsAuthenticated]
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

        # Extract the 'created_at' values
        created_at_values = [item['created_at'] for item in feedbacks]

        # Find the minimum and maximum 'created_at' valus    
        if not start_date:
            start_date = min(created_at_values)
        if not end_date:
            end_date = max(created_at_values)
         

        feedbacks = feedbacks.filter(Q(created_at__date__lte=end_date) & Q(created_at__date__gte=start_date))

        return Response(feedbacks)


class GetFeedbackProgress(APIView):
    permission_classes = [IsAuthenticated]
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

        # Extract the 'created_at' values
        created_at_values = [item['created_at'] for item in feedbacks]

        # Find the minimum and maximum 'created_at' valus    
        if not start_date:
            start_date = min(created_at_values)
        if not end_date:
            end_date = max(created_at_values)
         

        feedbacks = feedbacks.filter(Q(created_at__date__lte=end_date) & Q(created_at__date__gte=start_date))

        # print(feedbacks)
        total_yes += 0
        total_no += 0
        for i in feedbacks:
            print(i['question_answer'])

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
        course = self.request.GET.get('course', None) or None
        queryset = FeedbackQuestion.objects.values('course_name','chapter_name')

        if course:
            queryset = queryset.filter(course_name=course)
    
        # Create a defaultdict to group chapter names by course names
        # grouped_data = defaultdict(list)
        chapters = []
        # Group the chapter names under respective course names
        for item in queryset:
            course_name = item['course_name']
            chapter_name = item['chapter_name']
            # grouped_data[course_name].append(chapter_name)
            chapters.append(chapter_name)

        # return Response(grouped_data)
        return Response(chapters)

