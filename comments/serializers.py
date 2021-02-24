from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Comment, Review

User = get_user_model()


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    def validate(self, data):
        author = self.context.get('request').user
        title_id = self.context.get('view').kwargs['title_id']
        method = self.context.get('request').method
        if (Review.objects.filter(author=author, title=title_id)
                and method == 'POST'):
            raise serializers.ValidationError('Нельзя оставлять больше одного'
                                              'отзыва!')
        return data

    class Meta:
        fields = ['id', 'text', 'author', 'score', 'pub_date']
        read_only_fields = ('title',)
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = ['id', 'text', 'author', 'pub_date']
        read_only_fields = ('review',)
        model = Comment
