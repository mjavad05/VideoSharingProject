from rest_framework import serializers
from .models import User, Video, Subscription, WatchHistory,Comment, Rating
from django.contrib.auth import get_user_model


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_subscribed', 'subscription_type', 'subscription_end_date']


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'title', 'description', 'video_file', 'upload_date', 'status']


class SubscriptionSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')

    class Meta:
        model = Subscription
        fields = ['id', 'user', 'type_subscription', 'start_date', 'end_date', 'status']


class WatchHistorySerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')
    class Meta:
        model = WatchHistory
        fields = ['id', 'user', 'video', 'watch_date']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id' , 'text', 'created_at']
        read_only_fields = ['user', 'created_at']

    def create(self, validated_data):
        request = self.context['request']
        validated_data['user'] = request.user
        return super().create(validated_data)


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'rating', 'created_at']
        read_only_fields = ['user', 'created_at']

    def create(self, validated_data):
        request = self.context['request']
        validated_data['user'] = request.user
        return super().create(validated_data)