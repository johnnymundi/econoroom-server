from rest_framework import serializers
from .models import SavingsGoal, GoalDeposit


class GoalDepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoalDeposit
        fields = ('id', 'amount', 'note', 'created_at')
        read_only_fields = ('id', 'created_at')


class SavingsGoalSerializer(serializers.ModelSerializer):
    progress_percent = serializers.FloatField(read_only=True)
    remaining = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    deposits = GoalDepositSerializer(many=True, read_only=True)

    class Meta:
        model = SavingsGoal
        fields = ('id', 'name', 'target_amount', 'current_amount', 'remaining',
                  'progress_percent', 'deadline', 'status', 'created_at', 'completed_at', 'deposits')
        read_only_fields = ('id', 'current_amount', 'status', 'created_at', 'completed_at')
