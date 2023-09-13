from django.urls import path
from .views import (GetUsers, UserRegistrationView,UserLoginView,UserProfileView,
                    UserChangePasswordView,SendPasswordResetEmailView,UserPasswordResetView,User_logout,
                    TokenRefreshView,UsersDelete,Navbar,AlnafiUser,AllEmployees,GetUser,
                    GetNoOfUsersMonth,PSWFormRecord,IslamicUser,Marketing_Pkr_Form,Moc_leads_upload, NewAlnafiUser)
from django.http import HttpResponse

urlpatterns = [
    path("", lambda req: HttpResponse(status=200)),
    path('alnafiuser/',AlnafiUser.as_view(), name='alnafi-user'),
    path('islamicuser/',IslamicUser.as_view(), name='islamic-user'),
    path('userdelete/', UsersDelete.as_view(), name='user-delete'),
    # path("guacamoli/",Guacamoli.as_view(), name='guacamoli'),
    path('formrecord/', PSWFormRecord.as_view(), name='pswfform-record'),
    path('marketing_pkr_form/', Marketing_Pkr_Form.as_view(), name='marketing_pkr_form'),
    path('moc_leads_upload/', Moc_leads_upload.as_view(), name='moc-leads-upload'),

    path('users/', GetUsers.as_view(), name='user-list'),
    path('userdetails/<int:id>/', GetUser.as_view(), name='user-details'),
    path('nofusers/', GetNoOfUsersMonth.as_view(), name='no-of-users'),
    
    path('employees/', AllEmployees.as_view(), name='employees-list'),
    
    # path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('register/', UserRegistrationView.as_view()),
    path('login/', UserLoginView.as_view(),name='login'),
    path('logout/', User_logout,name='logout'),
    path('profile/', UserProfileView.as_view(),name='login'),
    path('changepassword/', UserChangePasswordView.as_view(),name='changepassword'),
    path('send-reset-password-email/', SendPasswordResetEmailView.as_view(),name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset-password'),
    path('newalnafiuser/', NewAlnafiUser.as_view, name='newalnfiuser'),
    path("navbar/", Navbar.as_view(), name='navbar'),
    # path('users/<int:pk>/', UserDetail.as_view(), name='user-detail'),
]
