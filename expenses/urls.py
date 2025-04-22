from django.urls import path
from . import views

urlpatterns = [
    path('groups/', views.groups, name='groups'),
    path('groups/create/', views.group_create, name='group-create'),
    path('groups/<int:group_id>/', views.group_detail, name='group-detail'),
    path('groups/<int:group_id>/edit/', views.group_edit, name='group-edit'),
    path('groups/<int:group_id>/delete/', views.group_delete, name='group-delete'),
    path('groups/<int:group_id>/invite/', views.group_invite, name='group-invite'),
    path('groups/join/<str:invite_code>/', views.group_join, name='group-join'),
    path('groups/join/', views.group_join_page, name='group-join-page'),
    path('groups/join-by-code/', views.group_join_by_code, name='group-join-code'),

    path('expenses/create/<int:group_id>/', views.expense_create, name='expense-create'),
    path('expenses/<int:expense_id>/', views.expense_detail, name='expense-detail'),
    path('expenses/<int:expense_id>/edit/', views.expense_edit, name='expense-edit'),
    path('expenses/<int:expense_id>/delete/', views.expense_delete, name='expense-delete'),

    path('settlements/<int:group_id>/', views.settlement_summary, name='settlement-summary'),
    path('settlements/<int:settlement_id>/mark-paid/', views.mark_settlement_paid, name='mark-settlement-paid'),

    path('export/pdf/<int:group_id>/', views.export_pdf, name='export-pdf'),
    path('export/excel/<int:group_id>/', views.export_excel, name='export-excel'),
]
