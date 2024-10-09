from rest_framework import viewsets
from .models import Video, Subscription, WatchHistory, Comment, Rating
from .serializers import VideoSerializer, SubscriptionSerializer, WatchHistorySerializer, RatingSerializer, CommentSerializer, UserRegisterSerializer, UserLoginSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework_simplejwt.views import TokenBlacklistView



class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]


class LoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(**serializer.validated_data)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response({'error': 'Invalid Credentials'}, status=400)


class LogoutView(TokenBlacklistView):
    permission_classes = [IsAuthenticated]


class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.filter(status='published')
    serializer_class = VideoSerializer
    permission_classes = [IsAuthenticated]


class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]


class WatchHistoryViewSet(viewsets.ModelViewSet):
    queryset = WatchHistory.objects.all()
    serializer_class = WatchHistorySerializer
    permission_classes = [IsAuthenticated]


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        video_pk = self.kwargs.get('video_pk')
        return Comment.objects.filter(video_id=video_pk)

    def perform_create(self, serializer):
        user = self.request.user
        video_id = self.kwargs.get('video_pk')
        serializer.save(user=user, video_id=video_id)


class RatingViewSet(viewsets.ModelViewSet):
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        video_pk = self.kwargs.get('video_pk')
        return Rating.objects.filter(video_id=video_pk)

    def perform_create(self, serializer):
        user = self.request.user
        video_id = self.kwargs.get('video_pk')
        serializer.save(user=user, video_id=video_id)
