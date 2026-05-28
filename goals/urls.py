from django.urls import path
from .views import SavingsGoalListCreateView, SavingsGoalDetailView, GoalDepositView

urlpatterns = [
    path('', SavingsGoalListCreateView.as_view(), name='goal-list'),
    path('<int:pk>/', SavingsGoalDetailView.as_view(), name='goal-detail'),
    path('<int:goal_id>/deposit/', GoalDepositView.as_view(), name='goal-deposit'),
]
