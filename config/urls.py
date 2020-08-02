from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from .views import index, health_check


urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('api/auth/', include('authentication.urls', namespace='authentication')),
    path('api/shitter/', include('shitter.urls', namespace='shitter')),
    path('healthy', health_check, name='healthy'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
