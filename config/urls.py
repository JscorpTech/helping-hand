"""
All urls configurations tree
"""

from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from config.env import env

################
# My apps url
################
urlpatterns = [
    path("", include("core.apps.accounts.urls")),
    path("chat/", include("core.apps.chat.urls")),
    path("news/", include("core.apps.news.urls")),
    path("sos/", include("core.apps.sos.urls")),
    path("education/", include("core.apps.education.urls")),
    path("shared/", include("core.apps.shared.urls")),
]


################
# Library urls
################
urlpatterns += [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("i18n/", include("django.conf.urls.i18n")),
    path("rosetta/", include("rosetta.urls")),
    path("ckeditor5/", include("django_ckeditor_5.urls"), name="ck_editor_5_upload_file"),
]

################
# Project env debug mode
################
if env.str("PROJECT_ENV") == "debug":
    urlpatterns += [path("silk/", include("silk.urls", namespace="silk"))]

    ################
    # Swagger urls
    ################
    urlpatterns += [
        path("schema/", SpectacularAPIView.as_view(), name="schema"),
        path("swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
        path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    ]

################
# Media urls
################
urlpatterns += [
    re_path(r"static/(?P<path>.*)", serve, {"document_root": settings.STATIC_ROOT}),
    re_path(r"media/(?P<path>.*)", serve, {"document_root": settings.MEDIA_ROOT}),
]
