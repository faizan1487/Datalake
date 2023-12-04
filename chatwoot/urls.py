from django.urls import path
from chatwoot.webhooks import user_created_webhook
from .views import ChatwootContacts, ConversationsReport, ConversationsList,InboxesList,AgentsList,AgentsReport,InboxesReport,Conversations,ConversationDetail

urlpatterns = [
    path("usercreatedwebhook/", user_created_webhook),
    path("chatwootuser/", ChatwootContacts.as_view(), name='chatwoot-user'),
    path("conversationreport/", ConversationsReport.as_view(), name='conversation-report'),

    path("conversationlist/", ConversationsList.as_view(), name='conversation-list'),
    path("conversations/", Conversations.as_view(), name='conversation'),
    path('conversationdetail/<int:id>/', ConversationDetail.as_view(), name='user-detail'),
    path("inboxlist/", InboxesList.as_view(), name='inboxes-list'),
    path("agentslist/", AgentsList.as_view(), name='agents-list'),
    path("agentsreport/", AgentsReport.as_view(), name='agent-report'),
    path("inboxesreport/", InboxesReport.as_view(), name='inboxes-report'),
]