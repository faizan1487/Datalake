from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from albaseer import settings

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("payments/",include('payment.urls')),
    path("user/",include('user.urls')),
    path("thinkific/",include('thinkific.urls')),
    path("products/",include('products.urls')),    
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
