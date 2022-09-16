from rest_framework import permissions
from .models import Category
from rest_framework.viewsets import ModelViewSet
from . import serializers
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination


# Create your views here.
class StandardResultPagination(PageNumberPagination):
    page_size = 5
    page_query_param = 'page'
    max_page_size = 1000


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = [permissions.IsAdminUser]

    filter_backends = (SearchFilter,)
    search_fields = ('username',)

    pagination_class = StandardResultPagination

    # def get_serializer_class(self):
    #     if self.action in ('retrieve',):
    #         return serializers.CategorySerializer
    #     elif self.action in ('create', 'update', 'partial_update'):
    #         return serializers.CategoryCreateSerializer
    #     else:
    #         return serializers.CategorySerializer
    #
    # def get_permissions(self):
    #     if self.action in ('create', 'update', 'partial_update', 'destroy'):
    #         return [permissions.IsAuthenticated(), permissions.IsAdminUser()]
    #     else:
    #         return [permissions.AllowAny()]
