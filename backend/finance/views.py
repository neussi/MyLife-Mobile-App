from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Sum, Q
from django.utils import timezone
from datetime import date
from .models import Category, Transaction, Budget
from .forms import CategoryForm, TransactionForm


@login_required
def finance_dashboard(request):
    today = timezone.localdate()
    month = int(request.GET.get('month', today.month))
    year = int(request.GET.get('year', today.year))

    transactions = Transaction.objects.filter(user=request.user, date__year=year, date__month=month)
    income = transactions.filter(type='INCOME').aggregate(total=Sum('amount'))['total'] or 0
    expense = transactions.filter(type='EXPENSE').aggregate(total=Sum('amount'))['total'] or 0
    balance = income - expense

    # By category for chart
    expense_by_cat = (
        transactions.filter(type='EXPENSE')
        .values('category__name', 'category__color')
        .annotate(total=Sum('amount'))
        .order_by('-total')
    )

    recent_transactions = Transaction.objects.filter(user=request.user).order_by('-date', '-created_at')[:10]
    categories = Category.objects.filter(user=request.user)

    return render(request, 'finance/dashboard.html', {
        'income': income,
        'expense': expense,
        'balance': balance,
        'transactions': recent_transactions,
        'expense_by_cat': list(expense_by_cat),
        'categories': categories,
        'month': month,
        'year': year,
        'today': today,
    })


@login_required
def transaction_list(request):
    transactions = Transaction.objects.filter(user=request.user)
    type_filter = request.GET.get('type', '')
    category_filter = request.GET.get('category', '')
    if type_filter:
        transactions = transactions.filter(type=type_filter)
    if category_filter:
        transactions = transactions.filter(category_id=category_filter)
    categories = Category.objects.filter(user=request.user)
    return render(request, 'finance/transaction_list.html', {
        'transactions': transactions,
        'categories': categories,
        'type_filter': type_filter,
        'category_filter': category_filter,
    })


@login_required
def transaction_create(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST, user=request.user)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            messages.success(request, "Transaction ajoutée.")
            return redirect('finance_dashboard')
    else:
        form = TransactionForm(user=request.user)
    return render(request, 'finance/transaction_form.html', {'form': form, 'title': 'Nouvelle Transaction'})


@login_required
def transaction_edit(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Transaction modifiée.")
            return redirect('finance_dashboard')
    else:
        form = TransactionForm(instance=transaction, user=request.user)
    return render(request, 'finance/transaction_form.html', {'form': form, 'title': 'Modifier la transaction'})


@login_required
def transaction_delete(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == 'POST':
        transaction.delete()
        messages.success(request, "Transaction supprimée.")
        return redirect('finance_dashboard')
    return render(request, 'includes/confirm_delete.html', {
        'object': f"{transaction.amount} FCFA - {transaction.description or transaction.category}",
        'type': 'transaction',
        'cancel_url': reverse('finance_dashboard')
    })


@login_required
def category_list(request):
    categories = Category.objects.filter(user=request.user)
    return render(request, 'finance/category_list.html', {'categories': categories})


@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            messages.success(request, "Catégorie créée.")
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'finance/category_form.html', {'form': form, 'title': 'Nouvelle Catégorie'})


@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk, user=request.user)
    if request.method == 'POST':
        category.delete()
        messages.success(request, "Catégorie supprimée.")
        return redirect('category_list')
    return render(request, 'includes/confirm_delete.html', {
        'object': category.name,
        'type': 'catégorie',
        'cancel_url': reverse('category_list')
    })


@login_required
def finance_chart_api(request):
    """API JSON pour les graphiques Chart.js."""
    year = int(request.GET.get('year', timezone.localdate().year))
    monthly_data = []
    for m in range(1, 13):
        income = Transaction.objects.filter(user=request.user, type='INCOME', date__year=year, date__month=m).aggregate(total=Sum('amount'))['total'] or 0
        expense = Transaction.objects.filter(user=request.user, type='EXPENSE', date__year=year, date__month=m).aggregate(total=Sum('amount'))['total'] or 0
        monthly_data.append({'month': m, 'income': float(income), 'expense': float(expense)})
    return JsonResponse({'monthly': monthly_data})
