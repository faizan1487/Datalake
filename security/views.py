from django.shortcuts import render
from django.template.loader import render_to_string
from django.db.models import Prefetch
from django.http import Http404
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

import environ
import pandas as pd
from datetime import datetime, timedelta, date
import os

env = environ.Env()
env.read_env()

# Create your views here.

class CreateScan(APIView):
    def get(self, request):
        scans = Scan.objects.values(
            'id', 'scan_type', 'scan_date', 'severity', 'remediation', 'assigned_to__name',
            'scan_progress', 'testing_method', 'target', 'target_value', 'application_type',
            'file_upload', 'poc'
        )
        scan_ids = [scan['id'] for scan in scans]

        # Prefetch comments and related data
        # comments = Comment.objects.select_related('department').prefetch_related('replies')
        # comments = comments.filter(scan_id__in=scan_ids)

        # comment_mapping = {}
        # for comment in comments:
        #     if comment.scan_id not in comment_mapping:
        #         comment_mapping[comment.scan_id] = []
        #     comment_mapping[comment.scan_id].append(comment)

        scan_data = []
        for scan in scans:
            scan_id = scan['id']

            if not scan['file_upload']:
                file_upload_link = ""
            else:
                file_upload_link = 'https://al-baseer.s3.us-east-2.amazonaws.com/' + scan['file_upload']
            
            if not scan['poc']:
                poc_link = ""
            else:
                poc_link = 'https://al-baseer.s3.us-east-2.amazonaws.com/' + scan['poc']

            scan_dict = {
                'id': scan_id,
                'scan_type': scan['scan_type'],
                'scan_date': scan['scan_date'],
                'severity': scan['severity'],
                'remediation': scan['remediation'],
                'assigned_to__name': scan['assigned_to__name'],
                'scan_progress': scan['scan_progress'],
                'testing_method': scan['testing_method'],
                'target': scan['target'],
                'target_value': scan['target_value'],
                'application_type': scan['application_type'],
                'file_upload': file_upload_link,
                'poc': poc_link,
                'no_of_comments': 0,
                'comments': [],
            }

            # if scan_id in comment_mapping:
            #     scan_dict['no_of_comments'] = len(comment_mapping[scan_id])
            #     scan_dict['comments'] = get_comments_data(comment_mapping[scan_id])

            scan_data.append(scan_dict)

        result = {"scans": scan_data}
        return Response(result)

    
    def post(self, request):
        data = request.data.copy()
        assigned_to_email = data.get('assigned_to')
        # print(assigned_to_email)
        # print(data)
        # print(data.get('file_upload'))
        scan_id = data.get('id')

        if assigned_to_email:
            try:
                department = Department.objects.get(name=data['assigned_to'])
                data['assigned_to'] = department.id
            except Department.DoesNotExist:
                data['assigned_to'] = None
        else:
            data['assigned_to'] = None
        
        try:
            instance = Scan.objects.get(id=scan_id)
            serializer = ScanSerializer(instance, data=data)
        except:
            serializer = ScanSerializer(data=data)

        # serializer.initial_data['file_upload_link'] = serializer.data['file_upload']
        # serializer.initial_data['poc_link'] = serializer.data['poc']

        if serializer.is_valid():
            # print(serializer.validated_data)
            serializer.save()

            serializer.data['file_upload_link'] == serializer.data['file_upload']
            serializer.data['poc_link'] == serializer.data['poc']
            print(serializer.data)

            if assigned_to_email:
                subject = 'Scan assigned to your department'
                params = {'subject': subject, 'scan_type': serializer.data['scan_type'], 'scan_date': serializer.data['scan_date'],
                        'severity': serializer.data['severity'], 'remediation': serializer.data['remediation'], 
                        'scan_progress': serializer.data['scan_progress'],'testing_method': serializer.data['testing_method'],
                        'target': serializer.data['target'], 'sub_target': serializer.data['target_value'], 'application_type': serializer.data['application_type']}
                html_content = render_to_string('emailtemplate.html', params)
                text_content = strip_tags(html_content)
                email_from = "secops@alnafi.edu.pk"
                recipient_list = department.email

                msg = EmailMultiAlternatives(subject, text_content, email_from, [
                                            recipient_list])
                msg.attach_alternative(html_content, "text/html")
                msg.send()
            # send_mail(subject, emailfrom, recipient_list)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)\
    
    
class ScanRetrieveUpdateDeleteAPIView(APIView):
    def get(self, request, pk):
        export = self.request.GET.get('export', None) or None
        try:
            # scan = Scan.objects.filter(id=pk).values()
            scan = Scan.objects.filter(id=pk).values(
            'id', 'scan_type', 'scan_date', 'severity', 'remediation', 'assigned_to__name',
            'scan_progress', 'testing_method', 'target', 'target_value', 'application_type',
            'file_upload', 'poc'
            )
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
                return Response(scan)
        except Scan.DoesNotExist:
            raise Http404



    # @permission_classes([IsAuthenticated])
    def put(self, request, pk):
        # data = request.data
        mutable_data = request.data.copy()
        assigned_to_email = mutable_data.get('assigned_to')

        if assigned_to_email:
            try:
                department = Department.objects.get(name=mutable_data['assigned_to'])
                mutable_data['assigned_to'] = department.id
            except User.DoesNotExist:
                mutable_data['assigned_to'] = None


        try:
            scan = Scan.objects.get(id=pk)
        except Scan.DoesNotExist:
            return Response("Scan not found", status=status.HTTP_404_NOT_FOUND)

        serializer = ScanSerializer(scan, data=mutable_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # @permission_classes([IsAuthenticated])
    def delete(self, request, pk):
        # scan = self.get_object(pk)
        scan = Scan.objects.get(id=pk)
        # if scan.user != request.user:
        #     return Response({"message":"You are not authorized to delete this scan"},status=status.HTTP_401_UNAUTHORIZED)
        scan.delete()
        return Response({"message":"scan Deleted!"},status=status.HTTP_204_NO_CONTENT)

class GetDepartment(APIView):
    def get(self, request):
        departments = Department.objects.values('name')
        print(departments)
        return Response(departments)

class CommentDelete(APIView):
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

