from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=5)
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=4, default=1.0)

    def __str__(self):
        return f'{self.code} ({self.symbol})'

    class Meta:
        verbose_name_plural = 'Currencies'

class Group(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='administered_groups')
    members = models.ManyToManyField(User, related_name='expense_groups')
    invite_code = models.CharField(max_length=36, unique=True, default=uuid.uuid4)
    image = models.ImageField(upload_to='group_images', default='default_group.jpg')

    def __str__(self):
        return self.name

    def get_total_expenses(self):
        return sum(expense.amount for expense in self.expenses.all())

    def get_member_count(self):
        return self.members.count()

class Expense(models.Model):
    SPLIT_CHOICES = [
        ('equal', 'Split Equally'),
        ('custom', 'Custom Split'),
    ]

    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='expenses')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    date = models.DateField(default=timezone.now)
    payer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='paid_expenses')
    split_type = models.CharField(max_length=10, choices=SPLIT_CHOICES, default='equal')
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, default=1)
    receipt = models.ImageField(upload_to='receipts', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.description} ({self.amount} {self.currency.code})'

    def get_participants(self):
        return [split.participant for split in self.splits.all()]

class ExpenseSplit(models.Model):
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name='splits')
    participant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expense_shares')
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.participant.username}: {self.amount} for {self.expense.description}'

class Settlement(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='settlements')
    payer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='settlements_to_pay')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='settlements_to_receive')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'{self.payer.username} owes {self.receiver.username} {self.amount} {self.currency.code}'

    def mark_as_paid(self):
        self.is_paid = True
        self.paid_at = timezone.now()
        self.save()
