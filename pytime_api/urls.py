from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from django.urls import path, include
from pytime_api import views

from core.urls import core_router
from core.views.health import HealthCheck

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', HealthCheck.as_view()),
    path('api/', include('authentication.urls'))
]

urlpatterns += core_router.urls
