from django.shortcuts import render
from rest_framework.views import APIView
# Create your views here.
from .models import ChatwoorUser
from django.http import HttpResponse
from threading import Thread
from rest_framework.response import Response
# Create your views here.
import requests

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
            print(user)
            user.save()


class Conversations(APIView):
    def get(self, request):
        url = 'https://chat.alnafi.com/api/v1/accounts/3/conversations/meta'
        api_access_token = '7M41q5QiNfYDeHue6KzjWdzV'

        headers = {
        'api_access_token': api_access_token,
        "Content-Type": "application/json",
        "Accept": "application/json",
        }
        response = requests.get(url, headers=headers)
        data = response.json()
        # print(data)
        return Response(data)