from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django.db.models import Sum
from django.utils import timezone
from .models import Category, Account, Transaction, Budget, Debt
from .serializers import CategorySerializer, AccountSerializer, TransactionSerializer, BudgetSerializer, DebtSerializer


class StandardPagination(PageNumberPagination):
    page_size = 20


class CategoryListCreateView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)


class AccountView(APIView):
    def get(self, request):
        account, _ = Account.objects.get_or_create(user=request.user)
        return Response(AccountSerializer(account).data)

    def patch(self, request):
        account, _ = Account.objects.get_or_create(user=request.user)
        serializer = AccountSerializer(account, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class TransactionListCreateView(generics.ListCreateAPIView):
    serializer_class = TransactionSerializer
    pagination_class = StandardPagination

    def get_queryset(self):
        qs = Transaction.objects.filter(user=self.request.user)
        type_filter = self.request.query_params.get('type')
        category = self.request.query_params.get('category')
        month = self.request.query_params.get('month')
        year = self.request.query_params.get('year')
        if type_filter:
            qs = qs.filter(type=type_filter)
        if category:
            qs = qs.filter(category_id=category)
        if month:
            qs = qs.filter(date__month=month)
        if year:
            qs = qs.filter(date__year=year)
        return qs

    def perform_create(self, serializer):
        transaction = serializer.save(user=self.request.user)
        account, _ = Account.objects.get_or_create(user=self.request.user)
        if transaction.type == Transaction.Type.INCOME:
            account.balance += transaction.amount
        else:
            account.balance -= transaction.amount
        account.save()


class TransactionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TransactionSerializer

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)


class SummaryView(APIView):
    def get(self, request):
        now = timezone.now()
        month = int(request.query_params.get('month', now.month))
        year = int(request.query_params.get('year', now.year))

        qs = Transaction.objects.filter(user=request.user, date__month=month, date__year=year)
        income = qs.filter(type='income').aggregate(total=Sum('amount'))['total'] or 0
        expenses = qs.filter(type='expense').aggregate(total=Sum('amount'))['total'] or 0

        by_category = (
            qs.filter(type='expense')
            .values('category__name', 'category__color')
            .annotate(total=Sum('amount'))
            .order_by('-total')
        )

        account, _ = Account.objects.get_or_create(user=request.user)

        return Response({
            'month': month,
            'year': year,
            'balance': account.balance,
            'income': income,
            'expenses': expenses,
            'net': income - expenses,
            'by_category': list(by_category),
        })


class BudgetListCreateView(generics.ListCreateAPIView):
    serializer_class = BudgetSerializer

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BudgetDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BudgetSerializer

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)


class DebtListCreateView(generics.ListCreateAPIView):
    serializer_class = DebtSerializer

    def get_queryset(self):
        return Debt.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DebtDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DebtSerializer

    def get_queryset(self):
        return Debt.objects.filter(user=self.request.user)
