from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Project Management Tool API",
        default_version="v1",
        description="API documentation for PMT",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="gopi.maganti1998@gmail.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Admin site
    path("admin/", admin.site.urls),
    # Your API endpoints (login/register/viewsets)
    path("api/", include("api.urls")),
    # Swagger/OpenAPI documentation
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
