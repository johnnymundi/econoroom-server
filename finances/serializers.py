from rest_framework import serializers
from .models import Category, Account, Transaction, Budget, Debt


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'icon', 'color', 'is_default')
        read_only_fields = ('id',)


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'balance', 'updated_at')
        read_only_fields = ('id', 'updated_at')


class TransactionSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Transaction
        fields = ('id', 'category', 'category_name', 'type', 'amount', 'description', 'date', 'created_at')
        read_only_fields = ('id', 'created_at')


class BudgetSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    spent = serializers.SerializerMethodField()

    class Meta:
        model = Budget
        fields = ('id', 'category', 'category_name', 'limit_amount', 'month', 'year', 'spent')
        read_only_fields = ('id',)

    def get_spent(self, obj):
        from django.db.models import Sum
        total = obj.category.transactions.filter(
            type='expense', date__month=obj.month, date__year=obj.year
        ).aggregate(total=Sum('amount'))['total']
        return total or 0


class DebtSerializer(serializers.ModelSerializer):
    remaining = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = Debt
        fields = ('id', 'creditor', 'total_amount', 'paid_amount', 'remaining', 'due_date', 'status', 'created_at', 'paid_at')
        read_only_fields = ('id', 'created_at', 'paid_at')
