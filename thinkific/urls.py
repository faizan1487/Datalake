from django.urls import path
from thinkific.webhooks import user_created_webhook

urlpatterns = [
    path("usercreatedwebhook/", user_created_webhook),
]