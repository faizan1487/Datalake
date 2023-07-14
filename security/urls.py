from django.urls import path
from .views import (CreateScan,ScanRetrieveUpdateDeleteAPIView,CommentDelete,GetDepartment)

urlpatterns = [
    path("createscan/", CreateScan.as_view(), name="scan_create"),
    path('get-update-deletescan/<int:pk>/', ScanRetrieveUpdateDeleteAPIView.as_view(), name='scan_delete'),
    path("deletecomment/", CommentDelete.as_view(), name="comment_delete"),
    path("departments/", GetDepartment.as_view(), name="departments"),
    # path('comments/create-update/', CommentCreateUpdateAPIView.as_view(), name='feedback_create'),
    # path("delete-comment/<int:pk>/", CommenetDeleteAPIView.as_view(), name="delete-comment"),
]