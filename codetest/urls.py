
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('teacher/', include('teacher.urls')),
    path('admin/', admin.site.urls),
]
