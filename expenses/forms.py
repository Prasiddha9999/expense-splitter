from django import forms
from django.forms import inlineformset_factory
from .models import Group, Expense, ExpenseSplit, Currency

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'description', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['amount', 'description', 'date', 'payer', 'split_type', 'currency', 'receipt']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.TextInput(attrs={'placeholder': 'What was this expense for?'}),
        }
    
    def __init__(self, *args, **kwargs):
        group = kwargs.pop('group', None)
        super(ExpenseForm, self).__init__(*args, **kwargs)
        
        if group:
            self.fields['payer'].queryset = group.members.all()

class ExpenseSplitForm(forms.ModelForm):
    class Meta:
        model = ExpenseSplit
        fields = ['participant', 'amount']
        widgets = {
            'amount': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
        }

# Create a formset for expense splits
ExpenseSplitFormSet = inlineformset_factory(
    Expense, 
    ExpenseSplit, 
    form=ExpenseSplitForm, 
    extra=1, 
    can_delete=True
)
