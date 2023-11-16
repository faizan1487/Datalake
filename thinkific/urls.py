from django.urls import path
from thinkific.webhooks import user_created_webhook,enrollment_created_webhook,progress_created_webhook, enrollment_completed_webhook
from .views import DeleteEnroll,GetThinkificUsers,GetUserEnrollments,ThinkificUsers, GetThinkificUser
urlpatterns = [
    path("enrollmentcompletewehbook/", enrollment_completed_webhook),
    path("usercreatedwebhook/", user_created_webhook),
    path("enrollmentcreatedwebhook/",enrollment_created_webhook),
    path("progress_created_webhook/", progress_created_webhook),
    path("deleteenroll/", DeleteEnroll.as_view()),
    path("thinkificusers/", GetThinkificUsers.as_view()),
    path("userenrollments/", GetUserEnrollments.as_view()),
    path("users/", ThinkificUsers.as_view()),

    path('thinkificuserdetails/<int:id>/', GetThinkificUser.as_view(), name='thinkific-user-details'),
]