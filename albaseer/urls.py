from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.views.generic import TemplateView
from albaseer import settings
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.schemas import get_schema_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path("chatwoot/",include('chatwoot.urls')),
    path("payments/",include('payment.urls')),
    path("user/",include('user.urls')),
    path("thinkific/",include('thinkific.urls')),
    path("products/",include('products.urls')),    
    path("trainers/",include('trainers.urls')),
    path("stream/",include('stream.urls')),
    path("affiliate/",include('affiliate.urls')),
    path("newsletter/",include('newsletter.urls')),    
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api_schema', get_schema_view(
                title="Al Baseer Rest APIs Documentation",
                description="Rest APIs for Al Baseer",
            ),
                name='api-schema'
            ),
    path('docs/', TemplateView.as_view(
            template_name='docs.html',
            extra_context={'schema_url': 'api-schema'}
        ), name='swagger-ui'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    # def trigger_error(request):
    #     1 / 0
    urlpatterns += [
        path('api_schema', get_schema_view(
                title="Al Baseer Rest APIs Documentation",
                description="Rest APIs for Al Baseer",
            ),
                name='api-schema'
            ),
        path('docs/', TemplateView.as_view(
                template_name='docs.html',
                extra_context={'schema_url': 'api-schema'}
            ), name='swagger-ui'),
        # path('sentry-debug/', trigger_error),  # type: ignore
        path('debug/', include('debug_toolbar.urls')), ]