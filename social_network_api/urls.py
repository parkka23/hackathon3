from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.routers import SimpleRouter
from post.views import PostViewSet
from category.views import CategoryViewSet
from django.conf.urls.static import static
from django.conf import settings

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Test API",
        default_version='v1',
        description="Social Network API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)
post_router = SimpleRouter()
post_router.register('posts', PostViewSet)

category_router = SimpleRouter()
category_router.register('categories', CategoryViewSet)

urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('api/v1/docs', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('admin/', admin.site.urls),
    path('api/v1/account/', include('account.urls')),
    path('api/v1/posts/', include('post.urls')),
    path('api/v1/', include(post_router.urls)),
    path('api/v1/', include(category_router.urls)),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += [path('', include('chat.urls')), ]
