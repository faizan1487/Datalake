from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
# Create your views here.
from .models import Newsletter
from django.db.models import Q


class MyPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 100  



class Subscribers(APIView):
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
        subscribers = Newsletter.objects.all().values()
        
        if q:
            subscribers = subscribers.filter(Q(email__icontains=q) | Q(full_name__icontains=q))

        if not start_date:
            first_subscriber = subscribers.exclude(created_at=None).last()
            start_date = first_subscriber['created_at'].date() if first_subscriber else None

        if not end_date:
            last_subscriber = subscribers.exclude(created_at=None).first()
            end_date = last_subscriber['created_at'].date() if last_subscriber else None




        paginator = MyPagination()
        paginated_queryset = paginator.paginate_queryset(subscribers, request)
        return paginator.get_paginated_response(paginated_queryset)
