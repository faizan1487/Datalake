from django.shortcuts import render
from rest_framework.views import APIView
# Create your views here.
from .models import ChatwoorUser
from django.http import HttpResponse
from threading import Thread
from rest_framework.response import Response
# Create your views here.
import requests
from datetime import datetime

class ChatwootUsers(APIView):
    def get(self, request):
        Thread(target=self.get_thread, args=(request,)).start()
        return HttpResponse("working")

    def get_thread(self, request):
        email_string = self.request.GET.get('emails', None) or None
        if email_string:
            emails = email_string.split(',')
            users = ChatwoorUser.objects.filter(email__in=emails)
        else:
            users = ChatwoorUser.objects.all()

        for user in users:
            # print(user)
            user.save()


class ConversationsReport(APIView):
    def get(self, request):
        params = {
            'type': 'account',
        }

        start_date = self.request.GET.get('start_date', None) or None
        if start_date:
            start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
            since = start_date_obj.timestamp()
            params['since'] = since
            print("since",since)

        end_date = self.request.GET.get('end_date', None) or None
        if end_date:
            end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
            until = end_date_obj.timestamp()
            params['until'] = until
            print("until",until)

        

        print(params)        
        # since=1689686153
        # until=1690204488
        type = 'account'

        api_access_token = '7M41q5QiNfYDeHue6KzjWdzV'


        headers = {
        'api_access_token': api_access_token,
        "Content-Type": "application/json",
        "Accept": "application/json",
        }
        url = 'https://chat.alnafi.com/api/v2/accounts/3/reports/summary'
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        print(data)
        return Response(data)