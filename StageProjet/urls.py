from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path,include

from StageProjet import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.reservation.urls")),
    
]
urlpatterns += staticfiles_urlpatterns()
