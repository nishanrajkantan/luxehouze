"""myapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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

from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('message', views.add_message),
    path('<int:m_id>', views.get_message),
    path('latest_message', views.get_latest_message),
    path('watch_info/<str:watch_model>', views.get_specific_watch_info),
    path('get_all_watch_info', views.get_all_watch_info),
    path('get_all_deals_info', views.get_all_deals_info),
    path('get_listing_info/<int:l_id>', views.get_listing_info),
]
