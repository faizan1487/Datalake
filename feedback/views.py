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

        if feedbacks:
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

        if feedbacks:
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
        else:
            feedbacks = feedbacks.filter(feedback_question_id__course_name='Mathematics A Level 9709')
        if chapter:
            feedbacks = feedbacks.filter(feedback_question_id__chapter_name=chapter)

        # print(feedbacks)
        if feedbacks:
            # Extract the 'created_at' values
            created_at_values = [item['created_at'] for item in feedbacks]

            # Find the minimum and maximum 'created_at' valus    
            if not start_date:
                start_date = min(created_at_values)
            if not end_date:
                end_date = max(created_at_values)
            
            feedbacks = feedbacks.filter(Q(created_at__date__lte=end_date) & Q(created_at__date__gte=start_date))

            total_yes = 0
            total_no = 0
            answers = []
            course_name = ''
            for i in feedbacks:
                course_name = i['feedback_question_id__course_name']
                data = i['question_answer']
                last_two_answers = data[-2:]
                # print(i)
                chapter_data = {'chapter_name': i['feedback_question_id__chapter_name'], 'answers': last_two_answers, 'user':i['user_email'],'created_at':i['created_at']}
                answers.append(chapter_data)
                for j in i['question_answer']:
                    if j['answer'].lower() == 'yes':
                        total_yes += 1
                    elif j['answer'].lower() == 'no':
                        total_no += 1

            yes_percent = total_yes/40 * 100
            no_percent = total_no/40 * 100


            # Define a dictionary to store the counts of 'Yes' and 'No' for each question
            question_counts = {}

            # Iterate over the queryset
            for feedback in feedbacks:
                # print(feedback)
                question_answers = feedback['question_answer']
                for answer_entry in question_answers:
                    answer = answer_entry['answer']
                    question = answer_entry['question']
                    
                    # Initialize counts for each question if not already done
                    if question not in question_counts:
                        question_counts[question] = {'Yes': 0, 'No': 0}
                    
                    # Increment the appropriate count
                    if answer == 'Yes':
                        question_counts[question]['Yes'] += 1
                    elif answer == 'No':
                        question_counts[question]['No'] += 1

            # print(question_counts)
            # Print the results
            # for question, counts in question_counts.items():
            #     print(f"Question: {question}")
            #     print(f"Yes: {counts['Yes']}")
            #     print(f"No: {counts['No']}")
            #     print("-" * 30)




            response_data = {'course_name': course_name,'yes': f'{yes_percent}%','no': f'{no_percent}%','answers':answers}
            return Response(response_data)
        
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

class GetCoursesUsers(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        course = self.request.GET.get('course', None) or None
        chapter = self.request.GET.get('chapter', None) or None
        queryset = FeedbackAnswers.objects.filter(feedback_question_id__course_name=course).values('user_email','feedback_question_id__chapter_name')
       
        if chapter:
            queryset = queryset.filter(feedback_question_id__chapter_name=chapter)

        emails = []
        for item in queryset:
            email = item['user_email']
            # grouped_data[course_name].append(chapter_name)
            emails.append(email)

        # return Response(grouped_data)
        return Response(emails)