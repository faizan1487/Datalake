from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import ScanSerializer,CommentSerializer
from .models import Scan, Comment
from user.models import User
from .services import get_comments_data
from django.db.models import Prefetch
from user.services import upload_csv_to_s3

import boto3
from django.conf import settings
import environ
from rest_framework.permissions import IsAuthenticated
import pandas as pd
from datetime import datetime, timedelta, date
import os
from django.http import Http404


env = environ.Env()
env.read_env()

# Create your views here.

class CreateScan(APIView):
    def get(self, request):
        scans = Scan.objects.values(
            'id', 'scan_type', 'scan_date', 'severity', 'remediation', 'assigned_to__email',
            'scan_progress', 'testing_method', 'target', 'http_or_https', 'application_type',
            'findings_and_recommendations', 'file_upload', 'poc'
        )
        scan_ids = [scan['id'] for scan in scans]

        # Prefetch comments and related data
        comments = Comment.objects.select_related('user').prefetch_related('replies')
        comments = comments.filter(scan_id__in=scan_ids)

        comment_mapping = {}
        for comment in comments:
            if comment.scan_id not in comment_mapping:
                comment_mapping[comment.scan_id] = []
            comment_mapping[comment.scan_id].append(comment)

        scan_data = []
        for scan in scans:
            scan_id = scan['id']
            scan_dict = {
                'id': scan_id,
                'scan_type': scan['scan_type'],
                'scan_date': scan['scan_date'],
                'severity': scan['severity'],
                'remediation': scan['remediation'],
                'assigned_to__email': scan['assigned_to__email'],
                'scan_progress': scan['scan_progress'],
                'testing_method': scan['testing_method'],
                'target': scan['target'],
                'http_or_https': scan['http_or_https'],
                'application_type': scan['application_type'],
                'findings_and_recommendations': scan['findings_and_recommendations'],
                'file_upload': 'https://alnafi-main-backend.s3.amazonaws.com/' + scan['file_upload'],
                'poc': 'https://alnafi-main-backend.s3.amazonaws.com/' + scan['poc'],
                'no_of_comments': 0,
                'comments': [],
            }

            if scan_id in comment_mapping:
                scan_dict['no_of_comments'] = len(comment_mapping[scan_id])
                scan_dict['comments'] = get_comments_data(comment_mapping[scan_id])

            scan_data.append(scan_dict)

        result = {"scans": scan_data}
        return Response(result)

    
    def post(self, request):
        data = request.data
        assigned_to_email = data.get('assigned_to')
        if assigned_to_email:
            try:
                team_member = User.objects.get(email=data['assigned_to'])
                data['assigned_to'] = team_member.id
            except User.DoesNotExist:
                data['assigned_to'] = None
        else:
            data['assigned_to'] = None
        serializer = ScanSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)\
    
    
class ScanRetrieveUpdateDeleteAPIView(APIView):
    def get(self, request, pk):
        export = self.request.GET.get('export', None) or None
        try:
            scan = Scan.objects.filter(id=pk).values()

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
        team_member = User.objects.get(email=mutable_data['assigned_to'])
        mutable_data['assigned_to'] = team_member.id

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



class CommentCreateUpdateAPIView(APIView):
    '''
        {
    "slug":"teseting-Scan",
    "comment":"kesy ho yr",
    "isPrimaryComment":true,
"parent_comment":3
    }
    '''

    # @permission_classes([IsAuthenticated])
    def post(self, request):
        mutable_data = request.data.copy()
        user = User.objects.first() if settings.DEBUG else request.user
        scan_id = request.data['scan_id']
        mutable_data['user'] = user.id
        mutable_data['scan'] = Scan.objects.get(id=scan_id).id
        serializer = CommentSerializer(data=mutable_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # @permission_classes([IsAuthenticated])
    def put(self, request):
        user = request.user.id
        comment_id = request.data['comment_id']
        comment = Comment.objects.get(id=comment_id)
        if comment:
            comment.comment = request.data['comment']
            comment.save()
            return Response({"message": "Comment Updated Successfully"}, status=status.HTTP_201_CREATED)
        return Response({"message": "Comment not found"}, status=status.HTTP_400_BAD_REQUEST)
   

class CommenetDeleteAPIView(APIView):
    # @permission_classes([IsAuthenticated])
    def delete(self, request, pk):
        try:
            comment = Comment.objects.get(id=pk)
            if comment.user != request.user:
                return Response({"message":"You are not authorized to delete this comment"},status=status.HTTP_401_UNAUTHORIZED)
            comment.delete()
            return Response({"message":"Comment Deleted!"},status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"message":"Comment not found!"},status=status.HTTP_400_BAD_REQUEST)

