from django.urls import path
from .views import (GetUserDetails, UserRegistrationView,UserLoginView,UserProfileView,
                    UserChangePasswordView,SendPasswordResetEmailView,UserPasswordResetView,User_logout,
                    TokenRefreshView,UsersDelete,GetNoOfUsers, Navbar,AlnafiUser)
from django.http import HttpResponse

urlpatterns = [
    path("", lambda req: HttpResponse(status=200)),
    path('alnafiuser/',AlnafiUser.as_view(), name='alnafi-user'),
    path('userdelete/', UsersDelete.as_view(), name='user-delete'),
    
    
    path('users/', GetUserDetails.as_view(), name='user-list'),
    path('nofusers/', GetNoOfUsers.as_view(), name='no-of-users'),
    
    
    # path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('register/', UserRegistrationView.as_view()),
    path('login/', UserLoginView.as_view(),name='login'),
    path('logout/', User_logout,name='logout'),
    path('profile/', UserProfileView.as_view(),name='login'),
    path('changepassword/', UserChangePasswordView.as_view(),name='changepassword'),
    path('send-reset-password-email/', SendPasswordResetEmailView.as_view(),name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset-password'),
    
    path("navbar/", Navbar.as_view(), name='navbar'),
    # path('users/<int:pk>/', UserDetail.as_view(), name='user-detail'),
]
