from django.urls import path
from chatwoot.webhooks import user_created_webhook
from .views import ChatwootContacts, ConversationsReport, ConversationsList,InboxesList,AgentsList

urlpatterns = [
    path("usercreatedwebhook/", user_created_webhook),
    # path("chatwootuser/", ChatwootContacts.as_view(), name='chatwoot-user'),
    path("conversationreport/", ConversationsReport.as_view(), name='conversation-report'),
    # path("inboxlist/", InboxesList.as_view(), name='inboxes-list'),
    # path("agentslist/", AgentsList.as_view(), name='agents-list'),
    # path("conversationlist/", ConversationsList.as_view(), name='conversation-list'),
]