from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from albaseer import settings
    
urlpatterns = [
    path('admin/', admin.site.urls),
    path("payments/",include('payment.urls')),
    path("",include('user.urls')),
    path("",include('thinkific.urls')),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
