"""codeonion-core URL Configuration

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
from django.urls import path
from main.views import home_view
from reporter.views import scan_status_view, repo_dependencies_view, repo_scan_status_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    # path('scan/', scan_home_view, name='scan_home'),
    path('scan_status/<repo_id>', scan_status_view, name='scan_status'),
    path('repo_dependencies/<uuid:repo_id>', repo_dependencies_view, name='repo_dependencies'),
    path('repo_scan_status/<uuid:repo_id>', repo_scan_status_view, name='repo_scan_status')
]