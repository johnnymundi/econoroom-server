from rest_framework import serializers
from .models import RoomItem, Achievement, UserAchievement, UserRoom


class RoomItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomItem
        fields = ('id', 'name', 'description', 'category', 'asset_key', 'position_x', 'position_y')


class AchievementSerializer(serializers.ModelSerializer):
    room_item = RoomItemSerializer(read_only=True)
    unlocked = serializers.SerializerMethodField()
    unlocked_at = serializers.SerializerMethodField()

    class Meta:
        model = Achievement
        fields = ('id', 'name', 'description', 'trigger_type', 'trigger_value', 'room_item', 'unlocked', 'unlocked_at')

    def get_unlocked(self, obj):
        request = self.context.get('request')
        if not request:
            return False
        return obj.user_achievements.filter(user=request.user).exists()

    def get_unlocked_at(self, obj):
        request = self.context.get('request')
        if not request:
            return None
        ua = obj.user_achievements.filter(user=request.user).first()
        return ua.unlocked_at if ua else None


class UserRoomSerializer(serializers.ModelSerializer):
    items = RoomItemSerializer(many=True, read_only=True)

    class Meta:
        model = UserRoom
        fields = ('id', 'items', 'updated_at')
