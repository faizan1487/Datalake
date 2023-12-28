from django.urls import path
from .views import (GetUsers, UserRegistrationView,UserLoginView,UserProfileView,
                    UserPasswordCheckTokenAPI,SendPasswordResetEmailView,User_logout,UsersDelete,Navbar,AlnafiUser,AllEmployees,
                    GetUser,GetNoOfUsersMonth,PSWFormRecord,IslamicUser,Marketing_Pkr_Form,Moc_leads_upload, NewAlnafiUser,UploadMocLeads,getUsser,
                    NewAlnafiUser,o_level_leads_moc_model,GetActiveUsers, UserSetNewPasswordAPIView, CvFormsApi, GetDataCV)
from django.http import HttpResponse

urlpatterns = [
    path("", lambda req: HttpResponse(status=200)),
    path('upload-moc-leads/',UploadMocLeads.as_view()),
    path('upload-o-level-leads/',o_level_leads_moc_model.as_view()),
    #below api ths is for moc leads
    path('getusers/',getUsser.as_view(), name='get-users'),

    path('alnafiuser/',AlnafiUser.as_view(), name='alnafi-user'),
    path('newalnafiuser/', NewAlnafiUser.as_view(), name='new-alnafi-user'), #for new mainsite users
    path('islamicuser/',IslamicUser.as_view(), name='islamic-user'),
    path('userdelete/', UsersDelete.as_view(), name='user-delete'),
    # path("guacamoli/",Guacamoli.as_view(), name='guacamoli'),
    path('formrecord/', PSWFormRecord.as_view(), name='pswfform-record'),
    path('marketing_pkr_form/', Marketing_Pkr_Form.as_view(), name='marketing_pkr_form'),
    path('moc_leads_upload/', Moc_leads_upload.as_view(), name='moc-leads-upload'),

    path('users/', GetUsers.as_view(), name='user-list'),
    path('getactiveusers/',GetActiveUsers.as_view(), name='get-active-users'),
    path('userdetails/<int:id>/', GetUser.as_view(), name='user-details'),
    path('nofusers/', GetNoOfUsersMonth.as_view(), name='no-of-users'),
    
    path('employees/', AllEmployees.as_view(), name='employees-list'),
    
    # path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('register/', UserRegistrationView.as_view()),
    path('login/', UserLoginView.as_view(),name='login'),
    path('logout/', User_logout,name='logout'),
    path('profile/', UserProfileView.as_view(),name='login'),
    path('send-reset-password-email/', SendPasswordResetEmailView.as_view(),name='send-reset-password-email'),
    
    path('user-password-rest/<uidb64>/<token>/', UserPasswordCheckTokenAPI.as_view(),name='changepassword'),
    path('changepassword/', UserSetNewPasswordAPIView.as_view()),

    path('newalnafiuser/', NewAlnafiUser.as_view(), name='newalnfiuser'),
    path("navbar/", Navbar.as_view(), name='navbar'),
    path("cv_form/", CvFormsApi.as_view()),
    path("cv_data/", GetDataCV.as_view()),
    # path('users/<int:pk>/', UserDetail.as_view(), name='user-detail'),
]
