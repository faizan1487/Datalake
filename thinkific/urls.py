from django.urls import path
from thinkific.webhooks import user_created_webhook

urlpatterns = [
    path("user-created-webhook/", user_created_webhook),
]