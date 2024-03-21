from django.shortcuts import render
from django.template.loader import render_to_string
from django.db.models import Prefetch
from django.http import Http404, HttpResponse
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.utils.html import strip_tags

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .serializers import ScanSerializer,CommentSerializer
from .models import Scan, Comment, Department
from user.models import User
from user.services import upload_csv_to_s3
import boto3
from rest_framework.permissions import IsAuthenticated
import environ
import pandas as pd
from datetime import datetime, timedelta, date
import os
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
import json



env = environ.Env()
env.read_env()

# Create your views here.
class MyPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 100           

class CreateScan(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        upcoming_scans = self.request.GET.get('upcoming_scans', None) or None
        status = self.request.GET.get('status', None) or None
        scans = Scan.objects.all().prefetch_related(Prefetch('assigned_to', queryset=Department.objects.all()))

        if upcoming_scans == 'true':
            scans = scans.filter(scan_date__gt=date.today())

        if status:
            scans = scans.filter(scan_progress=status)

        scan_data = []
        for scan in scans:
            if scan.file_upload:
                file_upload_link = scan.file_upload.url
            else:
                file_upload_link = ""

            if not scan.poc:
                poc_link = ""
            else:
                poc_link = scan.poc.url

            scan_dict = {
                'id': scan.id,
                'scan_type': scan.scan_type,
                'scan_date': scan.scan_date,
                'severity': scan.severity,
                'remediation': scan.remediation,
                'assigned_to': [department.name for department in scan.assigned_to.all()],
                'scan_progress': scan.scan_progress,
                'testing_method': scan.testing_method,
                'target': scan.target,
                'target_value': scan.target_value,
                'application_type': scan.application_type,
                'file_upload': file_upload_link,
                'poc': poc_link,
            }
            scan_data.append(scan_dict)

        # print(scan_data)
        # scan_ids = [scan['id'] for scan in scans]

        # Prefetch comments and related data
        # comments = Comment.objects.select_related('department').prefetch_related('replies')
        # comments = comments.filter(scan_id__in=scan_ids)

        # comment_mapping = {}
        # for comment in comments:
        #     if comment.scan_id not in comment_mapping:
        #         comment_mapping[comment.scan_id] = []
        #     comment_mapping[comment.scan_id].append(comment)

        # scan_data = []
        # for scan in scans:
        #     print(scan)
        #     scan_id = scan['id']

        #     if not scan['file_upload']:
        #         file_upload_link = ""
        #     else:
        #         file_upload_link = 'https://al-baseer.s3.us-east-2.amazonaws.com/' + scan['file_upload']
            
        #     if not scan['poc']:
        #         poc_link = ""
        #     else:
        #         poc_link = 'https://al-baseer.s3.us-east-2.amazonaws.com/' + scan['poc']

            # scan_dict = {
            #     'id': scan_id,
            #     'scan_type': scan['scan_type'],
            #     'scan_date': scan['scan_date'],
            #     'severity': scan['severity'],
            #     'remediation': scan['remediation'],
            #     'assigned_to__name': scan['assigned_to__name'],
            #     'scan_progress': scan['scan_progress'],
            #     'testing_method': scan['testing_method'],
            #     'target': scan['target'],
            #     'target_value': scan['target_value'],
            #     'application_type': scan['application_type'],
            #     'file_upload': file_upload_link,
            #     'poc': poc_link,
                # 'no_of_comments': 0,
                # 'comments': [],
            # }

            # if scan_id in comment_mapping:
            #     scan_dict['no_of_comments'] = len(comment_mapping[scan_id])
            #     scan_dict['comments'] = get_comments_data(comment_mapping[scan_id])

            # scan_data.append(scan_dict)

        # result = {"scans": scan_data}
        paginator = MyPagination()
        paginated_queryset = paginator.paginate_queryset(scan_data, request)        
        return paginator.get_paginated_response(paginated_queryset)
        # return Response(scans)

    permission_classes = [IsAuthenticated]
    def post(self, request):
        data = request.data.copy()
        assigned_to_names_str = data.get('assigned_to')
        # assigned_to_names_str = self.request.GET.get('assigned_to[]')

        if assigned_to_names_str is not None:
            assigned_to_names = assigned_to_names_str.split(',')
        
        scan_id = data.get('id')

        if assigned_to_names_str is not None:
            try:
                departments = Department.objects.filter(name__in=assigned_to_names)
                department_ids = [department.id for department in departments]
                data['assigned_to'] = department_ids
            except Department.DoesNotExist:
                data['assigned_to'] = None
        else:
            data['assigned_to'] = None

        
        data = {
            'scan_type': data['scan_type'] if 'scan_type' in data else None,
            'scan_date': data['scan_date'] if 'scan_date' in data else None,
            'severity': data['severity'] if 'severity' in data else None,
            'assigned_to': data['assigned_to'],
            'remediation': data['remediation'] if 'remediation' in data else None,
            'scan_progress': data['scan_progress'] if 'scan_progress' in data else None,
            'testing_method': data['testing_method'] if 'testing_method' in data else None,
            'target': data['target'] if 'target' in data else None,
            'target_value': data['target_value'] if 'target_value' in data else None,
            'file_upload': data['file_upload'] if 'file_upload' in data else None,
            'poc': data['poc'] if 'poc' in data else None,
            'application_type': data['application_type'] if 'application_type' in data else None
            }
        
        new_scan = Scan.objects.create(
            scan_type=data['scan_type'] if 'scan_type' in data else None,
            scan_date=data['scan_date'] if 'scan_date' in data else None,
            severity=data['severity'] if 'severity' in data else None,
            remediation= data['remediation'] if 'remediation' in data else None,
            scan_progress= data['scan_progress'] if 'scan_progress' in data else None,
            testing_method= data['testing_method'] if 'testing_method' in data else None,
            target= data['target'] if 'target' in data else None,
            target_value= data['target_value'] if 'target_value' in data else None,
            file_upload= data['file_upload'] if 'file_upload' in data else None,
            poc= data['poc'] if 'poc' in data else None
            )
        
        if data.get('assigned_to'):
            new_scan.assigned_to.set(data['assigned_to'])  

        assigned_to = [assign.name for assign in new_scan.assigned_to.all()]

        scan_data = {
            'id': new_scan.id,
            'assigned_to': assigned_to,
            'scan_type': new_scan.scan_type,
            'scan_date': new_scan.scan_date,
            'severity': new_scan.severity, 
            'remediation': new_scan.remediation, 
            'scan_progress': new_scan.scan_progress,
            'testing_method': new_scan.testing_method,
            'target': new_scan.target, 
            'sub_target': new_scan.target_value, 
            'application_type': new_scan.application_type,
            'file_upload': new_scan.file_upload.url if new_scan.file_upload and hasattr(new_scan.file_upload, 'url') else None,
            'poc':  new_scan.poc.url if new_scan.poc and hasattr(new_scan.poc, 'url') else None
        }

        if data.get('assigned_to'):
            subject = 'Vulnerability found.'
            params = {'subject': subject, 'scan_type': data['scan_type'], 'scan_date': data['scan_date'],
                    'severity': data['severity'], 'remediation': data['remediation'], 
                    'scan_progress': data['scan_progress'],'testing_method': data['testing_method'],
                    'target': data['target'], 'sub_target': data['target_value'], 'application_type': data['application_type']}
            html_content = render_to_string('emailtemplate.html', params)
            text_content = strip_tags(html_content)
            email_from = "secops@alnafi.edu.pk"
            recipient_list = []
            for department in departments:
                recipient_list.append(department.email)

            # msg = EmailMultiAlternatives(subject, text_content, email_from, recipient_list)
            # msg.attach_alternative(html_content, "text/html")
            # msg.send()

        return Response(scan_data, status=status.HTTP_201_CREATED)
    

class ScanRetrieveUpdateDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]  
    def get(self, request, pk):
        export = self.request.GET.get('export', None) or None
        try:
            scan = Scan.objects.filter(id=pk).prefetch_related(Prefetch('assigned_to', queryset=Department.objects.all()))
            if scan[0].file_upload:
                file_upload_link = scan[0].file_upload.url
            else:
                file_upload_link = ""

            if not scan[0].poc:
                poc_link = ""
            else:
                poc_link = scan[0].poc.url

            scan_dict = {
                'id': scan[0].id,
                'scan_type': scan[0].scan_type,
                'scan_date': scan[0].scan_date,
                'severity': scan[0].severity,
                'remediation': scan[0].remediation,
                'assigned_to': [department.name for department in scan[0].assigned_to.all()],
                'scan_progress': scan[0].scan_progress,
                'testing_method': scan[0].testing_method,
                'target': scan[0].target,
                'target_value': scan[0].target_value,
                'application_type': scan[0].application_type,
                'file_upload': file_upload_link,
                'poc': poc_link,
            }


            if export=='true':
                df = pd.DataFrame(scan)
                # Merge dataframes
                file_name = f"Scan_Data_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
                file_path = os.path.join(settings.MEDIA_ROOT, file_name)
                df = df.to_csv(index=False)
                s3 = upload_csv_to_s3(df,file_name)
                data = {'file_link': file_path,'export':'true'}
                return Response(data)
            else:
                return Response(scan_dict)
        except Scan.DoesNotExist:
            raise Http404



    permission_classes=[IsAuthenticated]
    def put(self, request, pk):
        data = request.data.copy()
        print(data)
        assigned_to_names_str = data.get('assigned_to')
        if assigned_to_names_str is not None:
            assigned_to_names = assigned_to_names_str.split(',')

        if assigned_to_names_str is not None:
            try:
                departments = Department.objects.filter(name__in=assigned_to_names)
                department_ids = [department.id for department in departments]
                data['assigned_to'] = department_ids
            except Department.DoesNotExist:
                data['assigned_to'] = None
        else:
            data['assigned_to'] = None

        try:
            scan = Scan.objects.get(id=pk)
            attributes_to_update = [
                'scan_type', 'scan_date','remediation', 'scan_progress', 'testing_method', 'target', 'target_value', 'application_type','severity'
            ]

            for attribute in attributes_to_update:
                if attribute in data:
                    setattr(scan, attribute, data[attribute])

            if 'file_upload' in data:
                scan.file_upload = data.get('file_upload', [None])

            if 'poc' in data:
                scan.poc = data.get('poc', [None])
            
            if data.get('assigned_to'):
                scan.assigned_to.set(data['assigned_to'])
            scan.save()

            assigned_to = [assign.name for assign in scan.assigned_to.all()]
            scan_data = {
                'id': scan.id,
                'assigned_to': assigned_to,
                'scan_type': scan.scan_type if scan.scan_type else None,
                'scan_date': scan.scan_date if scan.scan_date else None,
                'severity': scan.severity if scan.severity else None, 
                'remediation': scan.remediation if scan.remediation else None, 
                'scan_progress': scan.scan_progress if scan.scan_progress else None,
                'testing_method': scan.testing_method if scan.testing_method else None,
                'target': scan.target if scan.target else None, 
                'sub_target': scan.target_value if scan.target_value else None, 
                'application_type': scan.application_type if scan.application_type else None,
                'file_upload': scan.file_upload.url if scan.file_upload and hasattr(scan.file_upload, 'url') else None,
                'poc':  scan.poc.url if scan.poc and hasattr(scan.poc, 'url') else None
            }

            return Response(scan_data, status=status.HTTP_200_OK)
        except Scan.DoesNotExist:
            return Response("Scan not found", status=status.HTTP_404_NOT_FOUND)


    permission_classes = [IsAuthenticated]
    def delete(self, request, pk):
        # scan = self.get_object(pk)
        scan = Scan.objects.get(id=pk)
        # if scan.user != request.user:
        #     return Response({"message":"You are not authorized to delete this scan"},status=status.HTTP_401_UNAUTHORIZED)
        scan.delete()
        return HttpResponse("Scan Deleted!")
        return Response({"message":"Scan Deleted!"},status=status.HTTP_204_NO_CONTENT)

class GetDepartment(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        departments = Department.objects.values('name')
        # print(departments)
        return Response(departments)

class CommentDelete(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        objs = Scan.objects.all()
        objs.delete()
        return Response(' comments deleted')



# class CommentCreateUpdateAPIView(APIView):
#     '''
#         {
#     "slug":"teseting-Scan",
#     "comment":"kesy ho yr",
#     "isPrimaryComment":true,
# "parent_comment":3
#     }
#     '''

#     # @permission_classes([IsAuthenticated])
#     def post(self, request):
#         mutable_data = request.data.copy()
#         user = User.objects.first() if settings.DEBUG else request.user
#         scan_id = request.data['scan_id']
#         mutable_data['user'] = user.id
#         mutable_data['scan'] = Scan.objects.get(id=scan_id).id
#         serializer = CommentSerializer(data=mutable_data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     # @permission_classes([IsAuthenticated])
#     def put(self, request):
#         user = request.user.id
#         comment_id = request.data['comment_id']
#         comment = Comment.objects.get(id=comment_id)
#         if comment:
#             comment.comment = request.data['comment']
#             comment.save()
#             return Response({"message": "Comment Updated Successfully"}, status=status.HTTP_201_CREATED)
#         return Response({"message": "Comment not found"}, status=status.HTTP_400_BAD_REQUEST)
   

# class CommenetDeleteAPIView(APIView):
#     # @permission_classes([IsAuthenticated])
#     def delete(self, request, pk):
#         try:
#             comment = Comment.objects.get(id=pk)
#             if comment.user != request.user:
#                 return Response({"message":"You are not authorized to delete this comment"},status=status.HTTP_401_UNAUTHORIZED)
#             comment.delete()
#             return Response({"message":"Comment Deleted!"},status=status.HTTP_204_NO_CONTENT)
#         except Exception as e:
#             return Response({"message":"Comment not found!"},status=status.HTTP_400_BAD_REQUEST)

