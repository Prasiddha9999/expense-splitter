from django.contrib import admin
from .models import Currency, Group, Expense, ExpenseSplit, Settlement

class ExpenseSplitInline(admin.TabularInline):
    model = ExpenseSplit
    extra = 1

class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('description', 'amount', 'currency', 'date', 'payer', 'group')
    list_filter = ('date', 'currency', 'group')
    search_fields = ('description', 'payer__username', 'group__name')
    date_hierarchy = 'date'
    inlines = [ExpenseSplitInline]

class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'admin', 'created_at', 'get_member_count')
    list_filter = ('created_at',)
    search_fields = ('name', 'description', 'admin__username')
    filter_horizontal = ('members',)

class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'symbol', 'exchange_rate')
    search_fields = ('code', 'name')

class SettlementAdmin(admin.ModelAdmin):
    list_display = ('payer', 'receiver', 'amount', 'currency', 'is_paid', 'created_at')
    list_filter = ('is_paid', 'created_at', 'currency')
    search_fields = ('payer__username', 'receiver__username', 'group__name')
    date_hierarchy = 'created_at'

admin.site.register(Currency, CurrencyAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Settlement, SettlementAdmin)
