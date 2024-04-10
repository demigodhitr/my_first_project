from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404
from django.conf.urls import handler403
from django.conf.urls import handler500



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'myapp.views.custom404'
handler403 = 'myapp.views.custom403'
handler500 = 'myapp.views.custom500'



