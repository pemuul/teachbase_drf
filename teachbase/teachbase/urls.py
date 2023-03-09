"""teachbase URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from drf.views import DRF_API, TEACHBASE_API


router = routers.SimpleRouter()
router.register(r'drf', DRF_API)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)), # 'api/v1/drf/'
    path('api/v1/teachbase/', TEACHBASE_API.as_view()),
    path('', include('courser.urls'), name='courser'),
]