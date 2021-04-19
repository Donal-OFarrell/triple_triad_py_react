from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('triple_api/', include('triple_api.urls')),
    path('admin/', admin.site.urls),
]
