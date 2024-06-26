from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
# Create your views here.
from .models import StreamUser
from django.db.models import Q
from django.http import HttpResponse
from threading import Thread
from rest_framework.permissions import IsAuthenticated
class MyPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 100  


# permission_classes = [IsAuthenticated]
class StreamUsers(APIView):
    # permission_classes = [IsAuthenticated]
    # permission_classes = [GroupPermission]
    # required_groups = ['Sales', 'Admin']
    def get(self, request):
        q = self.request.GET.get('q', None) or None
        start_date = self.request.GET.get('start_date', None) or None
        end_date = self.request.GET.get('end_date', None) or None
        export = self.request.GET.get('export', None) or None
        url = request.build_absolute_uri()
        # payments = cache.get(url+'payments')
        # if payments is None:
        users = StreamUser.objects.all().values()
        
        if q:
            users = users.filter(Q(email__icontains=q) | Q(username__icontains=q))

        if not start_date:
            first_user = users.exclude(created_at=None).last()
            start_date = first_user['created_at'].date() if first_user else None

        if not end_date:
            last_user = users.exclude(created_at=None).first()
            end_date = last_user['created_at'].date() if last_user else None

        paginator = MyPagination()
        paginated_queryset = paginator.paginate_queryset(users, request)
        return paginator.get_paginated_response(paginated_queryset)


# permission_classes = [IsAuthenticated]
class UpdateStreamUser(APIView):
    def get(self, request):
        Thread(target=self.get_thread, args=(request,)).start()
        return HttpResponse("working")

    def get_thread(self, request):
        email_string = self.request.GET.get('emails', None) or None
        if email_string:
            emails = email_string.split(',')
            users = StreamUser.objects.filter(email__in=emails)
        else:
            users = StreamUser.objects.all()

        for user in users:
            print(user)
            user.save()