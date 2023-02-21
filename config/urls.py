from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', include('its_app.users.urls')),
    path('', include('its_app.projects.urls')),
    path('', include('its_app.issues.urls')),
    path('', include('its_app.comments.urls')),
]
