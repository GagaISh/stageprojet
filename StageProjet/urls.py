from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from django.views.i18n import set_language
from django.conf.urls.i18n import i18n_patterns
from rest_framework.authtoken import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('i18n/setlang/', set_language, name='set_language'),
   
]
urlpatterns += [
    path('api-token-auth/', views.obtain_auth_token)
]
urlpatterns += i18n_patterns(
    path("", include('apps.reservation.urls')),  
)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
