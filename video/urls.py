# video/urls.py
from django.urls import path
from .views import (VideoViewSet, SubscriptionViewSet,
                    WatchHistoryViewSet, CommentViewSet,
                    RatingViewSet,RegisterView,LoginView,LogoutView)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    path('api/videos/', VideoViewSet.as_view({'get': 'list', 'post': 'create'}), name='video-list'),
    path('api/videos/<int:pk>/', VideoViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),
         name='video-detail'),

    path('api/subscriptions/', SubscriptionViewSet.as_view({'get': 'list', 'post': 'create'}),
         name='subscription-list'),
    path('api/subscriptions/<int:pk>/',
         SubscriptionViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),
         name='subscription-detail'),

    path('api/history/', WatchHistoryViewSet.as_view({'get': 'list', 'post': 'create'}), name='history-list'),

    path('api/videos/<int:video_pk>/comments/', CommentViewSet.as_view({'get': 'list', 'post': 'create'}), name='video-comments'),

    path('api/videos/<int:video_pk>/ratings/', RatingViewSet.as_view({'get': 'list', 'post': 'create'}), name='video-ratings'),

]
