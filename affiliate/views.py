from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
# Create your views here.
from .models import AffiliateUser
from django.db.models import Q
from django.db.models import Count

class MyPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 100  





class AffiliateUsers(APIView):
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
        users = AffiliateUser.objects.annotate(user_clicks_count=Count('user_clicks')).values('first_name','last_name','email','phone','address','country','created_at','user_clicks_count')
        
        if q:
            users = users.filter(email__icontains=q)

        if not start_date:
            first_user = users.exclude(created_at=None).last()
            start_date = first_user['created_at'].date() if first_user else None

        if not end_date:
            last_user = users.exclude(created_at=None).first()
            end_date = last_user['created_at'].date() if last_user else None
        
        paginator = MyPagination()
        paginated_queryset = paginator.paginate_queryset(users, request)
        return paginator.get_paginated_response(paginated_queryset)