from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from comments.views import CommentsViewSet, ReviewsViewSet

from .views import CategoriesViewSet, GenresViewSet, TitlesViewSet

router = DefaultRouter()

router.register('genres', GenresViewSet)
router.register('categories', CategoriesViewSet)
router.register('titles', TitlesViewSet)
router.register('titles/(?P<title_id>\d+)/reviews', ReviewsViewSet, basename='reviews')
router.register('titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments', CommentsViewSet, basename='comments')

urlpatterns = [ 
    path('v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), 
    path('v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), 
    path('v1/', include(router.urls)), 
] 