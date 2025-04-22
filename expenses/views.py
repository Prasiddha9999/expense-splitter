import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.db.models import Sum, Q
from .models import Group, Expense, ExpenseSplit, Settlement, Currency
from .forms import GroupForm, ExpenseForm, ExpenseSplitFormSet
import json
import csv
import io
import xlsxwriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def home(request):
    # Direct HTML response without using Django templates
    # This ensures we don't have any template-related issues
    html = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Group Expense Splitter</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css">
        <style>
            body {
                font-family: 'Arial', sans-serif;
                background-color: #f9f9f9;
                color: #333;
            }
            .navbar {
                background-color: #FFD700 !important;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            .navbar-brand, .nav-link {
                color: #333 !important;
                font-weight: bold;
            }
            .hero {
                background-color: #FFD700;
                padding: 3rem 0;
                margin-bottom: 2rem;
            }
            .hero h1 {
                font-weight: bold;
                color: #333;
            }
            .feature-icon {
                display: inline-flex;
                align-items: center;
                justify-content: center;
                width: 4rem;
                height: 4rem;
                font-size: 2rem;
                border-radius: 50%;
                background-color: #FFD700;
                color: #333;
                margin-bottom: 1rem;
            }
            .card {
                border: none;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                transition: transform 0.3s ease;
                height: 100%;
            }
            .card:hover {
                transform: translateY(-5px);
            }
            .btn-primary {
                background-color: #FFD700;
                border-color: #FFD700;
                color: #333;
                font-weight: bold;
            }
            .btn-primary:hover {
                background-color: #FFC107;
                border-color: #FFC107;
                color: #333;
            }
            .btn-outline-primary {
                border-color: #FFD700;
                color: #333;
            }
            .btn-outline-primary:hover {
                background-color: #FFD700;
                border-color: #FFD700;
                color: #333;
            }
            footer {
                background-color: #333;
                color: white;
                padding: 2rem 0;
                margin-top: 3rem;
            }
        </style>
    </head>
    <body>
        <!-- Navigation -->
        <nav class="navbar navbar-expand-lg navbar-light">
            <div class="container">
                <a class="navbar-brand" href="/">Group Expense Splitter</a>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav ms-auto">
                        <li class="nav-item">
                            <a class="nav-link" href="/">Home</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/users/login/">Login</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/users/register/">Register</a>
                        </li>
                    </ul>
                </div>
            </div>
        </nav>

        <!-- Hero Section -->
        <section class="hero">
            <div class="container text-center">
                <h1 class="display-4">Split Expenses with Friends</h1>
                <p class="lead">Track who paid what and settle up without the hassle</p>
            </div>
        </section>

        <!-- Main Content -->
        <div class="container">
            <!-- Features Section -->
            <section class="py-5">
                <h2 class="text-center mb-5">How It Works</h2>
                <div class="row g-4">
                    <div class="col-md-4">
                        <div class="card p-4 text-center">
                            <div class="feature-icon mx-auto">
                                <i class="bi bi-people-fill"></i>
                            </div>
                            <h3>Create Groups</h3>
                            <p>Create groups for trips, events, or roommates. Invite friends to join and start tracking expenses together.</p>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="card p-4 text-center">
                            <div class="feature-icon mx-auto">
                                <i class="bi bi-cash-stack"></i>
                            </div>
                            <h3>Track Expenses</h3>
                            <p>Add expenses with details like amount, date, description, and receipt. Split equally or customize how much each person pays.</p>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="card p-4 text-center">
                            <div class="feature-icon mx-auto">
                                <i class="bi bi-calculator"></i>
                            </div>
                            <h3>Settle Up</h3>
                            <p>See who owes whom with our smart settlement calculator. Mark debts as paid and keep everyone on the same page.</p>
                        </div>
                    </div>
                </div>
            </section>

            <!-- CTA Section -->
            <section class="py-5 text-center">
                <h2 class="mb-4">Ready to Get Started?</h2>
                <div class="d-grid gap-2 d-md-flex justify-content-md-center">
                    <a href="/users/register/" class="btn btn-primary btn-lg px-4 me-md-2">Sign Up Now</a>
                    <a href="/users/login/" class="btn btn-outline-primary btn-lg px-4">Login</a>
                </div>
            </section>
        </div>

        <!-- Footer -->
        <footer>
            <div class="container text-center">
                <p>© 2025 Group Expense Splitter. All rights reserved.</p>
            </div>
        </footer>

        <!-- Bootstrap JS -->
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    '''
    return HttpResponse(html)

@login_required
def groups(request):
    user_groups = request.user.expense_groups.all()
    administered_groups = request.user.administered_groups.all()

    context = {
        'user_groups': user_groups,
        'administered_groups': administered_groups
    }

    return render(request, 'expenses/groups.html', context)

@login_required
def group_create(request):
    if request.method == 'POST':
        form = GroupForm(request.POST, request.FILES)
        if form.is_valid():
            group = form.save(commit=False)
            group.admin = request.user
            group.save()
            group.members.add(request.user)
            messages.success(request, f'Group "{group.name}" has been created!')
            return redirect('group-detail', group_id=group.id)
    else:
        form = GroupForm()

    return render(request, 'expenses/group_form.html', {'form': form, 'title': 'Create Group'})

@login_required
def group_detail(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    # Check if user is a member of the group
    if request.user not in group.members.all():
        messages.warning(request, 'You are not a member of this group.')
        return redirect('groups')

    expenses = group.expenses.all().order_by('-date')

    # Calculate total expenses
    total_expenses = expenses.aggregate(Sum('amount'))['amount__sum'] or 0

    # Calculate user's share
    user_paid = expenses.filter(payer=request.user).aggregate(Sum('amount'))['amount__sum'] or 0
    user_shares = ExpenseSplit.objects.filter(expense__group=group, participant=request.user).aggregate(Sum('amount'))['amount__sum'] or 0
    user_balance = user_paid - user_shares

    context = {
        'group': group,
        'expenses': expenses,
        'total_expenses': total_expenses,
        'user_paid': user_paid,
        'user_shares': user_shares,
        'user_balance': user_balance,
    }

    return render(request, 'expenses/group_detail.html', context)

@login_required
def group_edit(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    # Check if user is the admin of the group
    if request.user != group.admin:
        messages.warning(request, 'Only the group admin can edit the group.')
        return redirect('group-detail', group_id=group.id)

    if request.method == 'POST':
        form = GroupForm(request.POST, request.FILES, instance=group)
        if form.is_valid():
            form.save()
            messages.success(request, f'Group "{group.name}" has been updated!')
            return redirect('group-detail', group_id=group.id)
    else:
        form = GroupForm(instance=group)

    return render(request, 'expenses/group_form.html', {'form': form, 'title': 'Edit Group'})

@login_required
def group_delete(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    # Check if user is the admin of the group
    if request.user != group.admin:
        messages.warning(request, 'Only the group admin can delete the group.')
        return redirect('group-detail', group_id=group.id)

    if request.method == 'POST':
        group_name = group.name
        group.delete()
        messages.success(request, f'Group "{group_name}" has been deleted!')
        return redirect('groups')

    return render(request, 'expenses/group_confirm_delete.html', {'group': group})

@login_required
def group_invite(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    # Check if user is a member of the group
    if request.user not in group.members.all():
        messages.warning(request, 'You are not a member of this group.')
        return redirect('groups')

    invite_url = request.build_absolute_uri(f'/expenses/groups/join/{group.invite_code}/')

    return render(request, 'expenses/group_invite.html', {'group': group, 'invite_url': invite_url})

def group_join(request, invite_code):
    group = get_object_or_404(Group, invite_code=invite_code)

    if request.user.is_authenticated:
        if request.user in group.members.all():
            messages.info(request, f'You are already a member of {group.name}.')
        else:
            group.members.add(request.user)
            messages.success(request, f'You have joined {group.name}!')
        return redirect('group-detail', group_id=group.id)
    else:
        messages.info(request, 'Please log in to join the group.')
        return redirect('login')

@login_required
def expense_create(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    # Check if user is a member of the group
    if request.user not in group.members.all():
        messages.warning(request, 'You are not a member of this group.')
        return redirect('groups')

    if request.method == 'POST':
        form = ExpenseForm(request.POST, request.FILES, group=group)
        formset = ExpenseSplitFormSet(request.POST, prefix='splits')

        if form.is_valid() and formset.is_valid():
            expense = form.save(commit=False)
            expense.group = group
            expense.save()

            # Process splits
            total_split_amount = 0
            for split_form in formset:
                if split_form.cleaned_data.get('participant') and split_form.cleaned_data.get('amount'):
                    split = split_form.save(commit=False)
                    split.expense = expense
                    split.save()
                    total_split_amount += split.amount

            # Validate total split amount matches expense amount
            if total_split_amount != expense.amount:
                expense.delete()
                messages.error(request, 'The sum of splits must equal the total expense amount.')
                return render(request, 'expenses/expense_form.html', {'form': form, 'formset': formset, 'group': group})

            messages.success(request, f'Expense "{expense.description}" has been added!')
            return redirect('group-detail', group_id=group.id)
    else:
        form = ExpenseForm(initial={'payer': request.user}, group=group)
        formset = ExpenseSplitFormSet(prefix='splits')

    return render(request, 'expenses/expense_form.html', {'form': form, 'formset': formset, 'group': group})

@login_required
def expense_detail(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)
    group = expense.group

    # Check if user is a member of the group
    if request.user not in group.members.all():
        messages.warning(request, 'You are not a member of this group.')
        return redirect('groups')

    splits = expense.splits.all()

    context = {
        'expense': expense,
        'group': group,
        'splits': splits,
    }

    return render(request, 'expenses/expense_detail.html', context)

@login_required
def expense_edit(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)
    group = expense.group

    # Check if user is the payer or group admin
    if request.user != expense.payer and request.user != group.admin:
        messages.warning(request, 'Only the expense payer or group admin can edit this expense.')
        return redirect('expense-detail', expense_id=expense.id)

    if request.method == 'POST':
        form = ExpenseForm(request.POST, request.FILES, instance=expense, group=group)
        formset = ExpenseSplitFormSet(request.POST, prefix='splits', queryset=expense.splits.all())

        if form.is_valid() and formset.is_valid():
            expense = form.save()

            # Delete existing splits
            expense.splits.all().delete()

            # Process splits
            total_split_amount = 0
            for split_form in formset:
                if split_form.cleaned_data.get('participant') and split_form.cleaned_data.get('amount'):
                    split = split_form.save(commit=False)
                    split.expense = expense
                    split.save()
                    total_split_amount += split.amount

            # Validate total split amount matches expense amount
            if total_split_amount != expense.amount:
                messages.error(request, 'The sum of splits must equal the total expense amount.')
                return render(request, 'expenses/expense_form.html', {'form': form, 'formset': formset, 'group': group, 'expense': expense})

            messages.success(request, f'Expense "{expense.description}" has been updated!')
            return redirect('expense-detail', expense_id=expense.id)
    else:
        form = ExpenseForm(instance=expense, group=group)
        formset = ExpenseSplitFormSet(prefix='splits', queryset=expense.splits.all())

    return render(request, 'expenses/expense_form.html', {'form': form, 'formset': formset, 'group': group, 'expense': expense})

@login_required
def expense_delete(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)
    group = expense.group

    # Check if user is the payer or group admin
    if request.user != expense.payer and request.user != group.admin:
        messages.warning(request, 'Only the expense payer or group admin can delete this expense.')
        return redirect('expense-detail', expense_id=expense.id)

    if request.method == 'POST':
        group_id = group.id
        expense_desc = expense.description
        expense.delete()
        messages.success(request, f'Expense "{expense_desc}" has been deleted!')
        return redirect('group-detail', group_id=group_id)

    return render(request, 'expenses/expense_confirm_delete.html', {'expense': expense})

@login_required
def settlement_summary(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    # Check if user is a member of the group
    if request.user not in group.members.all():
        messages.warning(request, 'You are not a member of this group.')
        return redirect('groups')

    # Get all expenses for the group
    expenses = group.expenses.all()

    # Calculate balances for each member
    members = group.members.all()
    balances = {}

    for member in members:
        # Amount paid by the member
        paid = expenses.filter(payer=member).aggregate(Sum('amount'))['amount__sum'] or 0

        # Amount owed by the member
        shares = ExpenseSplit.objects.filter(expense__group=group, participant=member).aggregate(Sum('amount'))['amount__sum'] or 0

        # Calculate balance (positive means they are owed money, negative means they owe money)
        balances[member.id] = paid - shares

    # Calculate settlements
    settlements = []
    while any(abs(balance) > 0.01 for balance in balances.values()):
        # Find the member who owes the most money (most negative balance)
        payer_id = min(balances, key=balances.get)
        payer = next(m for m in members if m.id == payer_id)
        payer_balance = balances[payer_id]

        # Find the member who is owed the most money (most positive balance)
        receiver_id = max(balances, key=balances.get)
        receiver = next(m for m in members if m.id == receiver_id)
        receiver_balance = balances[receiver_id]

        # Skip if no one owes money or no one is owed money
        if payer_balance >= 0 or receiver_balance <= 0:
            break

        # Calculate the settlement amount
        amount = min(abs(payer_balance), receiver_balance)

        # Create a settlement record
        settlements.append({
            'payer': payer,
            'receiver': receiver,
            'amount': amount
        })

        # Update balances
        balances[payer_id] += amount
        balances[receiver_id] -= amount

    # Get existing settlements from the database
    db_settlements = Settlement.objects.filter(group=group)

    context = {
        'group': group,
        'members': members,
        'balances': balances,
        'settlements': settlements,
        'db_settlements': db_settlements,
    }

    return render(request, 'expenses/settlement_summary.html', context)

@login_required
def mark_settlement_paid(request, settlement_id):
    settlement = get_object_or_404(Settlement, id=settlement_id)
    group = settlement.group

    # Check if user is the payer or receiver
    if request.user != settlement.payer and request.user != settlement.receiver:
        messages.warning(request, 'Only the payer or receiver can mark this settlement as paid.')
        return redirect('settlement-summary', group_id=group.id)

    settlement.mark_as_paid()
    messages.success(request, f'Settlement of {settlement.amount} {settlement.currency.code} has been marked as paid!')

    return redirect('settlement-summary', group_id=group.id)

@login_required
def export_pdf(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    # Check if user is a member of the group
    if request.user not in group.members.all():
        messages.warning(request, 'You are not a member of this group.')
        return redirect('groups')

    # Create a file-like buffer to receive PDF data
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file"
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    # Add title
    styles = getSampleStyleSheet()
    elements.append(Paragraph(f"Group Expense Summary: {group.name}", styles['Title']))
    elements.append(Paragraph(f"Generated on: {timezone.now().strftime('%Y-%m-%d %H:%M')}", styles['Normal']))
    elements.append(Paragraph(f"Generated by: {request.user.username}", styles['Normal']))

    # Add expenses table
    expenses = group.expenses.all().order_by('-date')

    if expenses:
        elements.append(Paragraph("Expenses", styles['Heading2']))

        # Table data
        data = [
            ['Date', 'Description', 'Payer', 'Amount', 'Currency']
        ]

        for expense in expenses:
            data.append([
                expense.date.strftime('%Y-%m-%d'),
                expense.description,
                expense.payer.username,
                str(expense.amount),
                expense.currency.code
            ])

        # Create the table
        table = Table(data)

        # Add style
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.yellow),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ])

        table.setStyle(style)
        elements.append(table)

    # Add settlements
    settlements = Settlement.objects.filter(group=group)

    if settlements:
        elements.append(Paragraph("Settlements", styles['Heading2']))

        # Table data
        data = [
            ['Payer', 'Receiver', 'Amount', 'Currency', 'Status']
        ]

        for settlement in settlements:
            data.append([
                settlement.payer.username,
                settlement.receiver.username,
                str(settlement.amount),
                settlement.currency.code,
                'Paid' if settlement.is_paid else 'Unpaid'
            ])

        # Create the table
        table = Table(data)

        # Add style
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.yellow),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ])

        table.setStyle(style)
        elements.append(table)

    # Build the PDF
    doc.build(elements)

    # Get the value of the BytesIO buffer and write it to the response
    pdf = buffer.getvalue()
    buffer.close()

    # Create the HttpResponse object with the appropriate PDF headers
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{group.name}_expense_summary.pdf"'

    return response

@login_required
def export_excel(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    # Check if user is a member of the group
    if request.user not in group.members.all():
        messages.warning(request, 'You are not a member of this group.')
        return redirect('groups')

    # Create a file-like buffer to receive Excel data
    buffer = io.BytesIO()

    # Create a workbook and add a worksheet
    workbook = xlsxwriter.Workbook(buffer)
    worksheet = workbook.add_worksheet('Expenses')

    # Add a bold format to use to highlight cells
    bold = workbook.add_format({'bold': True, 'bg_color': '#FFD700', 'border': 1})
    date_format = workbook.add_format({'num_format': 'yyyy-mm-dd'})
    border = workbook.add_format({'border': 1})

    # Write headers
    worksheet.write(0, 0, 'Date', bold)
    worksheet.write(0, 1, 'Description', bold)
    worksheet.write(0, 2, 'Payer', bold)
    worksheet.write(0, 3, 'Amount', bold)
    worksheet.write(0, 4, 'Currency', bold)

    # Get expenses
    expenses = group.expenses.all().order_by('-date')

    # Write data rows
    for idx, expense in enumerate(expenses, start=1):
        worksheet.write_datetime(idx, 0, expense.date, date_format)
        worksheet.write(idx, 1, expense.description, border)
        worksheet.write(idx, 2, expense.payer.username, border)
        worksheet.write(idx, 3, float(expense.amount), border)
        worksheet.write(idx, 4, expense.currency.code, border)

    # Add a settlements worksheet
    settlements_sheet = workbook.add_worksheet('Settlements')

    # Write headers
    settlements_sheet.write(0, 0, 'Payer', bold)
    settlements_sheet.write(0, 1, 'Receiver', bold)
    settlements_sheet.write(0, 2, 'Amount', bold)
    settlements_sheet.write(0, 3, 'Currency', bold)
    settlements_sheet.write(0, 4, 'Status', bold)

    # Get settlements
    settlements = Settlement.objects.filter(group=group)

    # Write data rows
    for idx, settlement in enumerate(settlements, start=1):
        settlements_sheet.write(idx, 0, settlement.payer.username, border)
        settlements_sheet.write(idx, 1, settlement.receiver.username, border)
        settlements_sheet.write(idx, 2, float(settlement.amount), border)
        settlements_sheet.write(idx, 3, settlement.currency.code, border)
        settlements_sheet.write(idx, 4, 'Paid' if settlement.is_paid else 'Unpaid', border)

    # Add a summary worksheet
    summary_sheet = workbook.add_worksheet('Summary')

    # Write headers
    summary_sheet.write(0, 0, 'Member', bold)
    summary_sheet.write(0, 1, 'Total Paid', bold)
    summary_sheet.write(0, 2, 'Total Share', bold)
    summary_sheet.write(0, 3, 'Balance', bold)

    # Calculate balances for each member
    members = group.members.all()

    # Write data rows
    for idx, member in enumerate(members, start=1):
        # Amount paid by the member
        paid = expenses.filter(payer=member).aggregate(Sum('amount'))['amount__sum'] or 0

        # Amount owed by the member
        shares = ExpenseSplit.objects.filter(expense__group=group, participant=member).aggregate(Sum('amount'))['amount__sum'] or 0

        # Calculate balance
        balance = paid - shares

        summary_sheet.write(idx, 0, member.username, border)
        summary_sheet.write(idx, 1, float(paid), border)
        summary_sheet.write(idx, 2, float(shares), border)
        summary_sheet.write(idx, 3, float(balance), border)

    # Close the workbook before sending the data
    workbook.close()

    # Rewind the buffer
    buffer.seek(0)

    # Create the HttpResponse object with the appropriate Excel headers
    response = HttpResponse(buffer.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{group.name}_expense_summary.xlsx"'

    return response
