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



        users = Thinkific_User.objects.all().order_by('-created_at')
        # print(users)
        # print(q)
        if q:
            users = users.filter(email__icontains=q)
            
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

        if course_name:
            users = users.filter(user_enrollments__course_name=course_name).distinct()

        users = users.values("id","first_name","last_name","full_name","created_at","email","phone","user_enrollments__course_name")

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
        
        return Response([])
       

#From Bundle_id to courses names:
def get_courses_name_from_bundle_id(bundle_id):

    def get_courses(bundle_id, page=1):
        headers={
            "X-Auth-API-Key": '0af37f50be358db530e91f3033ca7b1d',
            "X-Auth-Subdomain": "alnafi",
            "Content-Type": "application/json"
            }

        # headers={
        #     "X-Auth-API-Key": '372ad45a3882e5f7dda23cd75d79556c',
        #     "X-Auth-Subdomain": "alnafidev",
        #     "Content-Type": "application/json"
        #     }
        
        #production url
        # f"https://api.thinkific.com/api/public/v1/bundles/{bundle_id}/courses?page={page}&limit=200",
        #stage url

        bundle_res = requests.get(
            f"https://api.thinkific.com/api/public/v1/bundles/{bundle_id}/courses?page={page}&limit=200",
            headers=headers
        ).json()
        return bundle_res
    # print("bundle_id",bundle_id)
    bundle_res = get_courses(bundle_id)
    # print("bundle_res",bundle_res)
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
        # url = "https://api.thinkific.com/api/public/v1/users?page=1&limit=25"
        # headers={
        #     "X-Auth-API-Key": '0af37f50be358db530e91f3033ca7b1d',
        #     "X-Auth-Subdomain": "alnafi",
        #     "Content-Type": "application/json"
        #     }
        
        response = requests.get(
                    f"https://api.thinkific.com/api/public/v1/users?page=&limit=1000",
                    headers={
                        "X-Auth-API-Key": '0af37f50be358db530e91f3033ca7b1d',
                        "X-Auth-Subdomain": "alnafi",
                        "Content-Type": "application/json"
                    })
        # response = requests.get(url, headers=headers)
        # print(response.status_code)
        json_data = json.loads(response.text)
        # print(len(json_data['items']))
        # limit=1000
        return Response(json_data)