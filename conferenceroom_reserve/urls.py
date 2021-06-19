"""conferenceroom_reserve URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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

from django.urls import path, re_path
from conroom_reserve_app.views import main_conf_reserve, room_conf_detail, room_conf_edit
urlpatterns = [
    path('admin/', admin.site.urls),
    path('crr/', main_conf_reserve),
    re_path(r'^crr/(?P<room_id>\d+)/?$', room_conf_detail),
    re_path(r'^crr/edit/(?P<room_id>\d+)/?$', room_conf_edit),
]
