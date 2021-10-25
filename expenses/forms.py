from django import forms
from expenses.models import Category, Expense
from django.utils.translation import gettext as _


class CreateExpense(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all())

    date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}))

    class Meta:
        model = Expense
        fields = ['amount', 'category', 'description', 'date']


class ExpenseUpdateForm(forms.ModelForm):

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
    )
    date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}))

    class Meta:
        model = Expense
        fields = ['amount', 'category', 'description', 'date']
