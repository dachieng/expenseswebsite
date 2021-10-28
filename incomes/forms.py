from django import forms
from incomes.models import UserIncome, Source


class UserIncomeCreationForm(forms.ModelForm):
    source = forms.ModelChoiceField(
        queryset=Source.objects.all())

    date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}))

    class Meta:
        model = UserIncome
        fields = ['amount', 'source', 'description', 'date']


class UserIncomeUpdateForm(forms.ModelForm):
    source = forms.ModelChoiceField(
        queryset=Source.objects.all())

    date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}))

    class Meta:
        model = UserIncome
        fields = ['amount', 'source', 'description', 'date']
