from django.urls import path
from chatwoot.webhooks import user_created_webhook
from .views import ChatwootUsers, Conversations

urlpatterns = [
    path("usercreatedwebhook/", user_created_webhook),
    path("chatwootuser/", ChatwootUsers.as_view(), name='chatwoot-user'),
    path("conversationcount/", Conversations.as_view(), name='conversation-count'),
]