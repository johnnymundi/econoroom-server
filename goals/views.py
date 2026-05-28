from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from django.utils import timezone
from .models import SavingsGoal, GoalDeposit
from .serializers import SavingsGoalSerializer, GoalDepositSerializer


class StandardPagination(PageNumberPagination):
    page_size = 20


class SavingsGoalListCreateView(generics.ListCreateAPIView):
    serializer_class = SavingsGoalSerializer
    pagination_class = StandardPagination

    def get_queryset(self):
        return SavingsGoal.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SavingsGoalDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SavingsGoalSerializer

    def get_queryset(self):
        return SavingsGoal.objects.filter(user=self.request.user)


class GoalDepositView(APIView):
    def post(self, request, goal_id):
        goal = get_object_or_404(SavingsGoal, id=goal_id, user=request.user)
        serializer = GoalDepositSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        deposit = serializer.save(goal=goal)
        goal.current_amount += deposit.amount
        if goal.current_amount >= goal.target_amount:
            goal.current_amount = goal.target_amount
            goal.status = SavingsGoal.Status.COMPLETED
            goal.completed_at = timezone.now()
        goal.save()

        return Response(SavingsGoalSerializer(goal).data, status=status.HTTP_201_CREATED)
