from django.urls import path
from thinkific.webhooks import user_created_webhook,enrollment_created_webhook
from .views import DeleteEnroll,GetThinkificUsers,GetUserEnrollments,ThinkificUsers
urlpatterns = [
    path("usercreatedwebhook/", user_created_webhook),
    path("enrollmentcreatedwebhook/",enrollment_created_webhook),
    path("deleteenroll/", DeleteEnroll.as_view()),
    path("thinkificusers/", GetThinkificUsers.as_view()),
    path("userenrollments/", GetUserEnrollments.as_view()),
    path("users/", ThinkificUsers.as_view())
]