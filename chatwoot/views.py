from django.shortcuts import render
from rest_framework.views import APIView
# Create your views here.
from .models import ChatwoorUser
from django.http import HttpResponse
from threading import Thread
# Create your views here.


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
            user.save()