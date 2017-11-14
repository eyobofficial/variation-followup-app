"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views
from django.contrib import admin

from dashboard import views as dashboard_views
from pages import views as pages_views

urlpatterns = [
    # Login to account URL mapper
    url(r'^login/$', auth_views.LoginView.as_view(), name='login'),

    # Logout URL mapper
    url(r'^logout/$', auth_views.logout_then_login, name='logout'),

    # User Registration URL mapper
    url(r'^signup/$', dashboard_views.signup, name='signup'),

    # Dashboard app mapper
    url(r'^dashboard/', include('dashboard.urls')),

    # Pages app mapper
    url(r'^$', pages_views.index, name='landing-page'),

    # Admin site mapper
    url(r'^admin/', admin.site.urls),
]
