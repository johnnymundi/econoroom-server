from django.urls import path
from .views import (
    CategoryListCreateView, CategoryDetailView,
    AccountView,
    TransactionListCreateView, TransactionDetailView,
    SummaryView,
    BudgetListCreateView, BudgetDetailView,
    DebtListCreateView, DebtDetailView,
)

urlpatterns = [
    path('categories/', CategoryListCreateView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('account/', AccountView.as_view(), name='account'),
    path('transactions/', TransactionListCreateView.as_view(), name='transaction-list'),
    path('transactions/<int:pk>/', TransactionDetailView.as_view(), name='transaction-detail'),
    path('summary/', SummaryView.as_view(), name='summary'),
    path('budgets/', BudgetListCreateView.as_view(), name='budget-list'),
    path('budgets/<int:pk>/', BudgetDetailView.as_view(), name='budget-detail'),
    path('debts/', DebtListCreateView.as_view(), name='debt-list'),
    path('debts/<int:pk>/', DebtDetailView.as_view(), name='debt-detail'),
]
