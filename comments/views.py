from django.shortcuts import get_object_or_404, render
from rest_framework import filters, permissions, serializers, viewsets
from rest_framework.pagination import PageNumberPagination

from content.models import Title

from .models import Comment, Review
from .permissions import IsAuthorOrAdminOrModerator
from .serializers import CommentSerializer, ReviewSerializer


class ReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, 
        IsAuthorOrAdminOrModerator
    ]

    def get_title(self):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        return title
      
    def get_queryset(self):
        title = self.get_title()
        return title.reviews.all()  

    def perform_create(self, serializers):
        title = self.get_title()
        serializers.save(author=self.request.user, title=title)


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, 
        IsAuthorOrAdminOrModerator
    ]

    def get_review(self):
        review = get_object_or_404(
            Review, 
            id=self.kwargs['review_id'], 
            title__id=self.kwargs['title_id']
        )
        return review

    def get_queryset(self):
        review = self.get_review()
        return review.comments.all()

    def perform_create(self, serializers):
        review = self.get_review()
        serializers.save(author=self.request.user, review=review)
