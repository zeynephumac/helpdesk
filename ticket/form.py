from django import forms
from .models import Ticket
from .models import IssueTitle

class CreatTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description']


class UpdateTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description']


class SolutionForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['solution']


class TicketForm(forms.Form):
    title = forms.ModelChoiceField(queryset=IssueTitle.objects.all())
    description = forms.CharField(widget=forms.Textarea)