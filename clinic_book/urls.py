
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('apps.accounts.urls')),
    
    path('api/v1/', include('apps.organizations.urls')),
    path('api/v1/', include('apps.patients.urls')),
    path('api/v1/', include('apps.doctors.urls')),
    # path('api/v1/', include('apps.appoinments.urls')),
]
