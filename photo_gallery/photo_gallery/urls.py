"""photo_gallery URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from core import views as gallery_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')), #path for allauth app
    path('',gallery_views.homepage, name="homepage"),
    path('<slug:username>/', gallery_views.gallery_list, name = 'gallery_list'),
    path('galleries', gallery_views.gallery_list),
    path('galleries/<int:gallery_pk>', gallery_views.gallery_detail, name = 'gallery_detail'),
    path('galleries/add', gallery_views.gallery_create, name = 'gallery_create'),
    path('galleries/<int:gallery_pk>/edit', gallery_views.gallery_update, name = 'gallery_update'),
    path('galleries/<int:gallery_pk>/delete', gallery_views.gallery_delete, name = 'gallery_delete'),
    path('photos/<int:gallery_pk>/add', gallery_views.photo_create, name='photo_create'),
    path('photos/<int:photo_pk>/', gallery_views.photo_detail, name='photo_detail'),
    path('photos/<int:photo_pk>/edit', gallery_views.photo_update, name='photo_update'),
    path('photos/<int:photo_pk>/delete', gallery_views.photo_delete, name='photo_delete'),

    #path('photos/<int:photo_pk>/comment', gallery_views.comment_create),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
        # For django versions before 2.0:
        # url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
