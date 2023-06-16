from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import ScanSerializer,CommentSerializer
from .models import Scan, Comment
from user.models import User
from .services import get_comments_data
# Create your views here.
import boto3
from django.conf import settings
import environ
from rest_framework.permissions import IsAuthenticated


env = environ.Env()
env.read_env()


class CreateScan(APIView):
    def get(self,request):
        scans = Scan.objects.values('id', 'scan_type', 'scan_date','severity','remediation',
                                    'assigned_to','scan_progress','testing_method','target','http_or_https',
                                    'application_type','findings_and_recommendations','file_upload','poc')
        for scan in scans:
            # print(scan)
            # print(scan['id'])
            scan['file_upload'] = 'https://alnafi-main-backend.s3.amazonaws.com/' + scan['file_upload']
            scan['poc'] = 'https://alnafi-main-backend.s3.amazonaws.com/' + scan['poc']

        result = {"scans": []}
        for scan in scans:
            scan_dict = dict(scan)
            scan_comments = Comment.objects.filter(
                scan_id=scan['id'], parent_comment=None)  # Get top-level comments
            comments_data = Comment.objects.filter(scan__id=scan['id']).values(
                'id', 'scan__id', 'parent_comment', 'isPrimaryComment', 'user__email', 'comment', 'created_at')
            comments = Comment.objects.filter(scan__id=scan['id']).count()
            scan_dict['no_of_comments'] = comments

            if scan_comments:
                comments_data = get_comments_data(scan_comments)
            scan_dict['comments'] = comments_data
            result['scans'].append(scan_dict)       

        return Response(result)
    
    def post(self, request):
        data = request.data
        # print(data)
        # print("type(data['file_upload'])",type(data['file_upload']))
        # print(data['poc'])
        # print(type(data['poc']))
        # print(data['assigned_to'])
        team_member = User.objects.get(email=data['assigned_to'])
        # print(team_member.id)
        data['assigned_to'] = team_member.id
        serializer = ScanSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)\
        
class ScanDeleteAPIView(APIView):
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
    "slug":"teseting-post",
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

