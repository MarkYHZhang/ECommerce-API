"""ShopifyDevChallenge URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls import url
from . import views
from . import settings


urlpatterns = [
    url(r'^retrieveProducts', views.retrieve_products),
    url(r'^createCart', views.create_cart),
    url(r'^checkoutCart', views.checkout_cart),
    url(r'^discardCart', views.discard_cart),
    url(r'^modifyCart', views.modify_cart),
    url(r'^getAccessToken$', views.access_token),
    url(r'^invalidateAccessToken$', views.invalidate_access_token),
]

handler404 = views.customhandler404
handler500 = views.customhandler500


if settings.ADMIN_ENABLED:
    urlpatterns += path('admin/', admin.site.urls)