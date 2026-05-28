from django.db import models
from django.conf import settings


class RoomItem(models.Model):
    class Category(models.TextChoices):
        FURNITURE = 'furniture', 'Móvel'
        DECORATION = 'decoration', 'Decoração'
        ELECTRONICS = 'electronics', 'Eletrônico'
        PLANT = 'plant', 'Planta'

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=Category.choices)
    asset_key = models.CharField(max_length=100, unique=True)
    position_x = models.FloatField(default=0)
    position_y = models.FloatField(default=0)

    def __str__(self):
        return self.name


class Achievement(models.Model):
    class TriggerType(models.TextChoices):
        GOAL_COMPLETED = 'goal_completed', 'Meta de economia concluída'
        DEBT_PAID = 'debt_paid', 'Dívida quitada'
        BUDGET_MONTHS = 'budget_months', 'Meses dentro do orçamento'
        TOTAL_SAVED = 'total_saved', 'Total poupado acumulado'
        FIRST_INCOME = 'first_income', 'Primeira receita registrada'

    name = models.CharField(max_length=150)
    description = models.CharField(max_length=255)
    trigger_type = models.CharField(max_length=30, choices=TriggerType.choices)
    trigger_value = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    room_item = models.OneToOneField(RoomItem, on_delete=models.SET_NULL, null=True, blank=True, related_name='achievement')

    def __str__(self):
        return self.name


class UserAchievement(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='achievements')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE, related_name='user_achievements')
    unlocked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'achievement')

    def __str__(self):
        return f'{self.user.email} — {self.achievement.name}'


class UserRoom(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='room')
    items = models.ManyToManyField(RoomItem, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Sala de {self.user.email} ({self.items.count()} itens)'
