from pickletools import decimalnl_long
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from .serializers import ThinkificUserSerializer,ThinkificUserEnrollmentSerializer
from rest_framework import status
import json 
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view
from rest_framework.decorators import renderer_classes
from user.models import AlNafi_User
from .models import Thinkific_Users_Enrollments
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse

@csrf_exempt
@api_view(['POST'])
@renderer_classes([JSONRenderer])
def user_created_webhook(request):
    if(request.method != "POST"):
        return HttpResponse(status=400)
    
    data = request.body
    data_string = data.decode('utf-8')
    json_data = json.loads(data_string)
    # print(json_data)
    email = json_data['payload']['email']

    user = AlNafi_User.objects.filter(email=email).values('phone')
    if user:
        # print(user)
        # print(user[0]['phone'])
        # print(user.phone)
        json_data['payload']['phone'] = user[0]['phone']

    # print(json_data)
    serializer = ThinkificUserSerializer(data=json_data['payload'])
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def formatdate(datestr):
    date_string=datestr
    substring = date_string[:19]
    new_substring = substring.replace('T', " ")
    return new_substring



#disable stage webhook from thinkific then production webhook will work
@csrf_exempt
@api_view(['POST'])
@renderer_classes([JSONRenderer])
def enrollment_created_webhook(request):
    print("enrollemnt created webhook")
    if(request.method != "POST"):
        return HttpResponse(status=400)
    
    data = request.body
    data_string = data.decode('utf-8')
    json_data = json.loads(data_string)
    print(json_data)
    payload_data = json_data['payload']
    created_at = payload_data['created_at']
    if created_at == None:
        pass
    else:
        formatted_date = formatdate(created_at)
        payload_data['created_at'] = formatted_date
    
    expiry_date = payload_data['expiry_date']
    if expiry_date == None:
        pass
    else:
        formatted_date = formatdate(expiry_date)
        payload_data['expiry_date'] = formatted_date
        
    completed_at = payload_data['completed_at']
    if completed_at == None:
        pass
    else:
        formatted_date = formatdate(completed_at)
        payload_data['completed_at'] = formatted_date
        
    started_at = payload_data['started_at']
    if started_at == None:
        pass
    else:
        formatted_date = formatdate(started_at)
        payload_data['started_at'] = formatted_date
        
    activated_at = payload_data['activated_at']
    if activated_at == None:
        pass
    else:
        formatted_date = formatdate(activated_at)
        payload_data['activated_at'] = formatted_date
        
    
    updated_at = payload_data['updated_at']
    if updated_at == None:
        pass
    else:
        formatted_date = formatdate(updated_at)
        payload_data['updated_at'] = formatted_date
    
    payload_data['user_id'] = json_data['payload']['user']['id']
    payload_data['first_name'] = json_data['payload']['user']['first_name']
    payload_data['last_name'] = json_data['payload']['user']['last_name']
    payload_data['email'] = json_data['payload']['user']['email']
    payload_data['course_id'] = json_data['payload']['course']['id']
    payload_data['course_name'] = json_data['payload']['course']['name']
    del payload_data['user']
    del payload_data['course']
    serializer = ThinkificUserEnrollmentSerializer(data=payload_data)
    
    try:
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        print(e)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






@csrf_exempt
@api_view(['POST'])
@renderer_classes([JSONRenderer])
def progress_created_webhook(request):
    print("progress webhook")
    if(request.method != "POST"):
        return HttpResponse(status=400)
    
    
    try:
        data = request.body
        data_string = data.decode('utf-8')
        json_data = json.loads(data_string)
        print(json_data)
        
        email = json_data.get('payload', {}).get('user', {}).get('email')
        course_id = json_data.get('payload', {}).get('course', {}).get('id')
        percentage = json_data.get('payload', {}).get('percentage_completed')
        percentage = float(percentage)
        percentage = percentage * 100

        print("email",email)
        print("course_id",course_id)
        print("percentage",percentage)
        print("percentage type", type(percentage))
        
        if not email or not course_id or percentage is None:
            return JsonResponse({'error': 'Invalid or missing data'}, status=400)
        
        try:
            enrollment = Thinkific_Users_Enrollments.objects.get(email=email, course_id=course_id)
            if percentage > enrollment.percentage_completed:
                enrollment.percentage_completed = percentage
                enrollment.save()
            return JsonResponse({'message': 'Enrollment updated successfully'}, status=200)
        except ObjectDoesNotExist:
            # Handle the case where the enrollment doesn't exist
            return JsonResponse({'error': 'Enrollment not found'}, status=404)
            
    except json.JSONDecodeError:
        # Handle JSON decoding error
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        # Handle other unexpected exceptions
        return JsonResponse({'error': 'An error occurred'}, status=500)
    

    
@csrf_exempt
@api_view(['POST'])
@renderer_classes([JSONRenderer])
def enrollment_completed_webhook(request):
    print("enrollment completion webhook")
    if request.method != "POST":
        return HttpResponse(status=400)
    
    try:
        data = json.loads(request.body.decode('utf-8'))  # Parsing JSON directly
        # print(data)

        payload = data.get('payload', {})
        user_data = payload.get('user', {})
        course_data = payload.get('course', {})

        email = user_data.get('email')
        course_id = course_data.get('id')

        if not email or course_id is None:
            return JsonResponse({'error': 'Invalid or missing data'}, status=400)

        try:
            enrollment = Thinkific_Users_Enrollments.objects.get(email=email, course_id=course_id)
            enrollment.status = 'Completed'
            enrollment.save()
            return JsonResponse({'message': 'Completed'}, status=200)
        except Thinkific_Users_Enrollments.DoesNotExist:
            return JsonResponse({'error': 'Enrollment not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': 'An error occurred: ' + str(e)}, status=500)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'error': 'An error occurred: ' + str(e)}, status=500)