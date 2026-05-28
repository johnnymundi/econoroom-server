from django.urls import path
from .views import AchievementListView, UserRoomView

urlpatterns = [
    path('achievements/', AchievementListView.as_view(), name='achievement-list'),
    path('room/', UserRoomView.as_view(), name='user-room'),
]
