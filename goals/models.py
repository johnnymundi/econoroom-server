from django.db import models
from django.conf import settings


class SavingsGoal(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'active', 'Ativa'
        COMPLETED = 'completed', 'Concluída'
        CANCELLED = 'cancelled', 'Cancelada'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='savings_goals')
    name = models.CharField(max_length=150)
    target_amount = models.DecimalField(max_digits=12, decimal_places=2)
    current_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    deadline = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    @property
    def progress_percent(self):
        if self.target_amount == 0:
            return 0
        return min(round((self.current_amount / self.target_amount) * 100, 1), 100)

    @property
    def remaining(self):
        return max(self.target_amount - self.current_amount, 0)

    def __str__(self):
        return f'{self.user.email} — {self.name} ({self.progress_percent}%)'


class GoalDeposit(models.Model):
    goal = models.ForeignKey(SavingsGoal, on_delete=models.CASCADE, related_name='deposits')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    note = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.goal.name} +R${self.amount}'
