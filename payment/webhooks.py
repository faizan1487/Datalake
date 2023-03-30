from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response

@csrf_exempt
def enrollment_created_webhook(request):
    if(request.method != "POST"):
        return HttpResponse(status=400)
    data = request.body
    # print(data)
    return HttpResponse(status=200)