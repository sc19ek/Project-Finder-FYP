"""ProjectFinder URL Configuration

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
from django.urls import path
from PFapp.views import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name="index"),
    path('associate_login', associate_login, name="associate_login"),
    path('resourcer_login', resourcer_login, name="resourcer_login"),
    path('user_signup', user_signup, name="user_signup"),
    path('Logout', Logout, name="Logout")
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
