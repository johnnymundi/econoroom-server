from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Sum
from finances.models import Transaction, Debt
from goals.models import SavingsGoal
from .models import Achievement, UserAchievement, UserRoom


def _unlock_achievement(user, trigger_type, trigger_value=None):
    qs = Achievement.objects.filter(trigger_type=trigger_type)
    if trigger_value is not None:
        qs = qs.filter(trigger_value__lte=trigger_value)

    for achievement in qs:
        ua, created = UserAchievement.objects.get_or_create(user=user, achievement=achievement)
        if created and achievement.room_item:
            room, _ = UserRoom.objects.get_or_create(user=user)
            room.items.add(achievement.room_item)


@receiver(post_save, sender=Transaction)
def check_first_income(sender, instance, created, **kwargs):
    if created and instance.type == Transaction.Type.INCOME:
        count = Transaction.objects.filter(user=instance.user, type=Transaction.Type.INCOME).count()
        if count == 1:
            _unlock_achievement(instance.user, Achievement.TriggerType.FIRST_INCOME)


@receiver(post_save, sender=SavingsGoal)
def check_goal_completed(sender, instance, **kwargs):
    if instance.status == SavingsGoal.Status.COMPLETED:
        completed_count = SavingsGoal.objects.filter(
            user=instance.user, status=SavingsGoal.Status.COMPLETED
        ).count()
        _unlock_achievement(instance.user, Achievement.TriggerType.GOAL_COMPLETED, completed_count)

        total_saved = SavingsGoal.objects.filter(
            user=instance.user, status=SavingsGoal.Status.COMPLETED
        ).aggregate(total=Sum('target_amount'))['total'] or 0
        _unlock_achievement(instance.user, Achievement.TriggerType.TOTAL_SAVED, total_saved)


@receiver(post_save, sender=Debt)
def check_debt_paid(sender, instance, **kwargs):
    if instance.status == Debt.Status.PAID:
        paid_count = Debt.objects.filter(
            user=instance.user, status=Debt.Status.PAID
        ).count()
        _unlock_achievement(instance.user, Achievement.TriggerType.DEBT_PAID, paid_count)
