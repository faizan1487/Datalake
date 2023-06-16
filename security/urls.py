from django.urls import path
from .views import CreateScan,CommentCreateUpdateAPIView,CommenetDeleteAPIView,ScanDeleteAPIView

urlpatterns = [
    path("createscan/", CreateScan.as_view(), name="scan_create"),
    path('deletescan/<int:pk>/', ScanDeleteAPIView.as_view(), name='scan_delete'),
    path('comments/create-update/', CommentCreateUpdateAPIView.as_view(), name='feedback_create'),
    path("delete-comment/<int:pk>/", CommenetDeleteAPIView.as_view(), name="delete-comment"),
]