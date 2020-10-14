from django.conf.urls import url
from django.contrib import admin
from django.urls import path

from core.urls import core_router
from core.views.health import HealthCheck

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', HealthCheck.as_view()),
]

urlpatterns += core_router.urls
