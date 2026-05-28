from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Achievement, UserRoom
from .serializers import AchievementSerializer, UserRoomSerializer


class AchievementListView(generics.ListAPIView):
    serializer_class = AchievementSerializer
    queryset = Achievement.objects.select_related('room_item').prefetch_related('user_achievements')

    def get_serializer_context(self):
        return {**super().get_serializer_context(), 'request': self.request}


class UserRoomView(APIView):
    def get(self, request):
        room, _ = UserRoom.objects.get_or_create(user=request.user)
        return Response(UserRoomSerializer(room).data)
