from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, viewsets
from django.db.models import Avg

from .filters import TitleFilter
from .models import Category, Genre, Title
from .permissions import IsAdminOrReadOnly
from .serializers import (CategoriesSerializer, GenreSerializer,
                          TitlesSerializer, TitlesSerializerGet)


class MixinView(mixins.CreateModelMixin,
                mixins.DestroyModelMixin,
                mixins.ListModelMixin,
                viewsets.GenericViewSet):
    pass


class GenresViewSet(MixinView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name']
    lookup_field = 'slug'
    http_method_names = ['get', 'post', 'delete']
    permission_classes = [IsAdminOrReadOnly, ]


class CategoriesViewSet(MixinView):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name']
    http_method_names = ['get', 'post', 'delete']
    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly, ]


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter
    permission_classes = [IsAdminOrReadOnly, ]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitlesSerializerGet
        else:
            return TitlesSerializer
