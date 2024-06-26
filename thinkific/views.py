from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from .models import Thinkific_Users_Enrollments, Thinkific_User
from .serializers import ThinkificUserSerializer,ThinkificUserEnrollmentSerializer
from rest_framework.permissions import IsAuthenticated
import requests
import json
from payment.models import Main_Payment
from user.models import Main_User
from datetime import datetime, timedelta
from django.db.models import Q
import pandas as pd
from django.conf import settings
from user.services import upload_csv_to_s3
import os
from rest_framework import status


# Create your views here.
class MyPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 100  


class DeleteEnroll(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        objs = Thinkific_Users_Enrollments.objects.all()
        objs.delete()
        return Response("data deleted")   
    
class GetThinkificUsers(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request): 
        q = self.request.GET.get('q', None) or None
        start_date = self.request.GET.get('start_date', None) or None
        req_end_date = self.request.GET.get('end_date', None) or None
        course_name = self.request.GET.get('course_name', None) or None
        export = self.request.GET.get('export', None) or None



        users = Thinkific_User.objects.all().order_by('-created_at')
        # print(users)
        # print(q)
        if q:
            users = users.filter(email__icontains=q)

        if course_name:
            users = users.filter(user_enrollments__course_name=course_name).distinct()

        # print(users)

        if not start_date:
            first_user = users.exclude(created_at=None).last()
            if first_user and first_user.created_at:
                date_time_obj = first_user.created_at.strftime("%Y-%m-%d %H:%M:%S.%f")
                new_date_obj = datetime.strptime(date_time_obj, "%Y-%m-%d %H:%M:%S.%f")
                start_date = new_date_obj
                start_date = start_date.date()

       
        if not req_end_date:
            last_user = users.exclude(created_at=None).first()
            if last_user and last_user.created_at:
                date_time_obj = last_user.created_at.strftime("%Y-%m-%d %H:%M:%S.%f")
                new_date_obj = datetime.strptime(date_time_obj, "%Y-%m-%d %H:%M:%S.%f")
                end_date = new_date_obj
                end_date = end_date.date()
                end_date = end_date + timedelta(days=1)

        if req_end_date:
            end_date = datetime.strptime(req_end_date, "%Y-%m-%d")
            end_date = end_date + timedelta(days=1)

        users = users.filter(Q(created_at__gte = start_date) & Q(created_at__lte = end_date))


        users = users.values("id","first_name","last_name","full_name","created_at","email","phone","user_enrollments__course_name")


        if export == 'true':
            file_name = f"Thinkific_Users_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
            file_path = os.path.join(settings.MEDIA_ROOT, file_name)
            df = pd.DataFrame(users).to_csv(index=False)
            s3 = upload_csv_to_s3(df, file_name)
            data = {'file_link': file_path, 'export': 'true'}
            return Response(data)
        else:    
            paginator = MyPagination()
            paginated_queryset = paginator.paginate_queryset(users, request)
            return paginator.get_paginated_response(paginated_queryset)




class GetThinkificUser(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id):
        user_id = id
        user = Thinkific_User.objects.filter(id=user_id)

        # print(user)
        # print("user[0].email",user[0].email)

        payments = Main_Payment.objects.filter(user__email=user[0].email)

        # print(payments)
        if payments:
            # print("payments",payments)
            #extract prodcuts from those payments
            #extract bundle ids from those products
            bundle_ids = payments.values('product__bundle_ids','product__product_name')
            # print("bundle_ids",bundle_ids)
            #this make a get request to thinkific bundle api and extract courses names from api response
            courses  = []
            for i in bundle_ids:
                if i['product__bundle_ids']:
                    if i['product__bundle_ids'] != '7869':
                        bundle_courses = get_courses_name_from_bundle_id(i['product__bundle_ids'])
                        bundle_courses['bundle_id'] = i['product__bundle_ids']
                        bundle_courses['product_name'] = i['product__product_name']
                        courses.append(bundle_courses)
            

            # print("courses",courses)
            #then calculate the total progress of the bunble from individual courses
            #then send those individual courses and total progress of bundle in api response
            enrollments = user[0].user_enrollments.all().values()

            # print("enrollments",enrollments)

            # Extract courses from both querysets
            # print("courses",courses)
            courses_queryset = courses[0]['courses_details']
            enrollments_queryset = [item['course_name'] for item in enrollments]

            # Create a dictionary to store courses based on product_name
            courses_dict = {}

            # Iterate through the courses in the first queryset
            for course in courses_queryset:
                course_name = course['course_name']
                product_name = courses[0]['product_name']
                
                # Check if the course is also present in the second queryset
                if course_name in enrollments_queryset:
                    # If the product_name is not already a key in the dictionary, add it
                    if product_name not in courses_dict:
                        courses_dict[product_name] = []
                    # Append the course to the list of courses for the current product_name
                    courses_dict[product_name].append(course_name)

            # Iterate through the courses in the second queryset
            for course_name in enrollments_queryset:
                if any(course_name in courses_list for courses_list in courses_dict.values()):
                    pass
                else:
                    # If not, add it to the dictionary with a default key (e.g., 'No Product Name')
                    if 'Independant Course' not in courses_dict:
                        courses_dict['Independant Course'] = []
                    courses_dict['Independant Course'].append(course_name)

        # Create a dictionary to store extracted information
            result_dict = {}

            # Extract and save percentage completed for each course
            for key, courses_list in courses_dict.items():
                for course_name in courses_list:
                    matching_courses = [entry for entry in enrollments if entry['course_name'] == course_name]
                    for matching_course in matching_courses:
                        result_key = f"{key} - {course_name}"
                        result_value = matching_course['percentage_completed']
                    
                        result_dict[result_key] = result_value

        # Create a list to store dictionaries representing categories
            organized_data = []

            for key, value in result_dict.items():
                # Extract the category (e.g., 'CAT Half yearly' or 'Independant Course')
                category = key.split(' - ')[0]

                # Check if the category is already in the list
                category_dict = next((d for d in organized_data if d['bundle'] == category), None)

                # If the category is not in the list, add it
                if not category_dict:
                    category_dict = {'bundle': category, 'courses': [], 'average_percentage': 0}
                    organized_data.append(category_dict)

                # Append the course and percentage to the corresponding category in the list
                category_dict['courses'].append({'course': key, 'percentage': value})

            # Calculate the average percentage for each category
            for category_dict in organized_data:
                if category_dict['courses']:
                    category_dict['average_percentage'] = sum(course['percentage'] for course in category_dict['courses']) / len(category_dict['courses'])

            return Response(organized_data)

        else:
            enrollments = user[0].user_enrollments.all().values()

            enrollments_queryset = [item['course_name'] for item in enrollments]

            # Create a dictionary to store courses based on product_name
            courses_dict = {}

            # Iterate through the courses in the second queryset
            for course_name in enrollments_queryset:
                if any(course_name in courses_list for courses_list in courses_dict.values()):
                    pass
                else:
                    # If not, add it to the dictionary with a default key (e.g., 'No Product Name')
                    if 'Independant Course' not in courses_dict:
                        courses_dict['Independant Course'] = []
                    courses_dict['Independant Course'].append(course_name)

        # Create a dictionary to store extracted information
            result_dict = {}

            # Extract and save percentage completed for each course
            for key, courses_list in courses_dict.items():
                for course_name in courses_list:
                    matching_courses = [entry for entry in enrollments if entry['course_name'] == course_name]
                    for matching_course in matching_courses:
                        result_key = f"{key} - {course_name}"
                        result_value = matching_course['percentage_completed']
                    
                        result_dict[result_key] = result_value

        # Create a list to store dictionaries representing categories
            organized_data = []

            for key, value in result_dict.items():
                # Extract the category (e.g., 'CAT Half yearly' or 'Independant Course')
                category = key.split(' - ')[0]

                # Check if the category is already in the list
                category_dict = next((d for d in organized_data if d['bundle'] == category), None)

                # If the category is not in the list, add it
                if not category_dict:
                    category_dict = {'bundle': category, 'courses': [], 'average_percentage': 0}
                    organized_data.append(category_dict)

                # Append the course and percentage to the corresponding category in the list
                category_dict['courses'].append({'course': key, 'percentage': value})

            # Calculate the average percentage for each category
            for category_dict in organized_data:
                if category_dict['courses']:
                    category_dict['average_percentage'] = sum(course['percentage'] for course in category_dict['courses']) / len(category_dict['courses'])

            return Response(organized_data)

        # return Response([])
       

#From Bundle_id to courses names:
def get_courses_name_from_bundle_id(bundle_id):

    def get_courses(bundle_id, page=1):
       
        bundle_res = requests.get(
            f"https://api.thinkific.com/api/public/v1/bundles/{bundle_id}/courses?page={page}&limit=200",
            headers=headers
        ).json()
        return bundle_res
    bundle_res = get_courses(bundle_id)
    # current_page = bundle_res.get("meta").get("pagination").get("current_page")
    total_pages = bundle_res.get("meta").get("pagination").get("total_pages")
    total_items = bundle_res.get("meta").get("pagination").get("total_items")

    bundle_data = {}
    bundle_data["total_courses"] = total_items
    course_details = []
    def get_items(bundle_res):

        for item in bundle_res.get("items"):
            course_details.append({
                "course_name": item.get("name"),
                "course_id": item.get("id")
            })

        bundle_data["courses_details"] = course_details
        return bundle_data

    data = get_items(bundle_res)
    if total_pages > 1:
        for i in range(2, total_pages+1):
            bundle_res = get_courses(bundle_id, i)
            data_page = get_items(bundle_res)
            course_details.extend(data_page["courses_details"])
    return data


class GetUserEnrollments(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        query = self.request.GET.get('q', None) or None
        # queryset = Thinkific_Users_Enrollments.objects.filter(email__iexact=query)
        queryset = Thinkific_Users_Enrollments.objects.all()
        paginator = MyPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        user_enrollemnt_serializer = ThinkificUserEnrollmentSerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(user_enrollemnt_serializer.data)    


class ThinkificUsers(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        
        response = requests.get(
                    f"https://api.thinkific.com/api/public/v1/users?page=&limit=1000",
                    headers={
                        "Content-Type": "application/json"
                    })
        # response = requests.get(url, headers=headers)
        # print(response.status_code)
        json_data = json.loads(response.text)
        # print(len(json_data['items']))
        # limit=1000
        return Response(json_data)
    




class SaveThinkificUsers(APIView):
   def post(self,request):
        data = request.data
        for i in range(100):
            full_name = data['full_name'][i]
            email = data['email'][i]
            id = data['id'][i]
            first_name = data['first_name'][i]
            last_name = data['last_name'][i]
            created_at = data['created_at'][i]
            phone = data['phone'][i]
            company = data['company'][i]
            roles = data['roles'][i]
            avatar_url = data['avatar_url'][i]
            bio = data['bio'][i]
            headline = data['headline'][i]
            affiliate_code = data['affiliate_code'][i]
            external_source = data['external_source'][i]
            affiliate_commission = data['affiliate_commission'][i]
            affiliate_commission_type = data['affiliate_commission_type'][i]
            affiliate_payout_email = data['affiliate_payout_email'][i]
            administered_course_ids = data['administered_course_ids'][i]
            custom_profile_fields = data['custom_profile_fields'][i]
            

            user, created = Thinkific_User.objects.get_or_create(email=email, defaults={
                'first_name': first_name,
                'last_name': last_name,
                'full_name':full_name,
                'phone': phone,
                'email': email,
                'id': id,
                'company':company,
                'roles': roles,
                'created_at': created_at,
                'avatar_url':avatar_url,
                'bio':bio,
                'headline':headline,
                'affiliate_code':affiliate_code,
                'external_source':external_source,
                'affiliate_commission':affiliate_commission,
                'affiliate_commission_type':affiliate_commission_type,
                'affiliate_payout_email':affiliate_payout_email,
                'administered_course_ids':administered_course_ids,
                'custom_profile_fields':custom_profile_fields,
            })

            # If the object was not created (i.e., it already existed), update its attributes
            if not created:
                user.first_name = first_name
                user.last_name = last_name
                user.full_name = full_name
                user.created_at = created_at
                user.phone = phone
                user.email = email
                user.id = id
                user.company = company
                user.roles = roles
                user.headline = headline
                user.affiliate_code = affiliate_code
                user.bio = bio
                user.external_source = external_source
                user.affiliate_commission = affiliate_commission
                user.affiliate_commission_type = affiliate_commission_type
                user.affiliate_payout_email = affiliate_payout_email
                user.administered_course_ids = administered_course_ids
                user.custom_profile_fields = custom_profile_fields
                user.avatar_url = avatar_url
                user.save()


        return Response("done")

class SaveEnrollments(APIView):
    def post(self, request): 
        data = request.data
        for i in range(len(data['first_name'])):
            user_id = data['user_id'][i]
            user_instance = Thinkific_User.objects.get(id=user_id)
            user_data = {
                'id': data['id'][i],
                'created_at': data['created_at'][i],
                'expiry_date': data['expiry_date'][i],
                'percentage_completed': data['percentage_completed'][i],
                'completed_at': data['completed_at'][i],
                'free_trial': data['free_trial'][i],
                'started_at': data['started_at'][i],
                'activated_at': data['activated_at'][i],
                'updated_at': data['updated_at'][i],
                'user_id': user_instance,
                'first_name': data['first_name'][i],
                'last_name': data['last_name'][i],
                'email': data['email'][i],
                'course_id': data['course_id'][i],
                'course_name': data['course_name'][i],
            }
            enrollment, created = Thinkific_Users_Enrollments.objects.get_or_create(user_id=user_instance, course_name=data['course_name'][i], defaults=user_data)


            if not created:
                enrollment.first_name = user_data['first_name']
                enrollment.last_name = user_data['last_name']
                enrollment.created_at = user_data['created_at']
                enrollment.email = user_data['email']
                enrollment.id = user_data['id']
                enrollment.expiry_date = user_data['expiry_date']
                enrollment.percentage_completed = user_data['percentage_completed']
                enrollment.completed_at = user_data['completed_at']
                enrollment.free_trial = user_data['free_trial']
                enrollment.started_at = user_data['started_at']
                enrollment.activated_at = user_data['activated_at']
                enrollment.updated_at = user_data['updated_at']
                enrollment.course_id = user_data['course_id']
                enrollment.course_name = user_data['course_name']
                enrollment.save()

        return Response("done")
