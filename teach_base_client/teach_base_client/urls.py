from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('authorization.urls')),
    path('api/', include(('api.urls', 'api'), namespace='api')),
    path('', include(('client.urls', 'client'), namespace='client')),
]
