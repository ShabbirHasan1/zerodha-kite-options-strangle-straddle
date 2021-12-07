from django import forms
from django.forms import widgets
from .models import Strategy


class StrategyForm(forms.ModelForm):
    entry_time = forms.TimeField(required=True, input_formats=["%I:%M %p", ])
    exit_time = forms.TimeField(required=True, input_formats=["%I:%M %p", ])
    class Meta:
        model = Strategy
        fields = [
            'name',
            'underlying',
            'strategy',
            'difference',
            'entry_time',
            'exit_time',
            'stop_loss_type',
            'stop_loss',
            'move_sl_to_cost',
            'active'
        ]
    
    def __init__(self, *args, **kwargs):
        super(StrategyForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs = {
            'class': 'form-control',
            'placeholder': 'Enter name'
        }
        self.fields['underlying'].widget.attrs = {
            'class': 'form-control',
            'placeholder': 'Enter Underlying'
        }
        self.fields['strategy'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter Strategy'
        })
        self.fields['difference'].widget.attrs = {
            'class': 'form-control',
            'placeholder': 'Enter Difference'
        }
        self.fields['entry_time'].widget.attrs = {
            'class': 'form-control datetimepicker-input',
            'placeholder': 'Enter Entry Time',
            "data-target": "#id_entry_time",
        }
        self.fields['exit_time'].widget.attrs = {
            'class': 'form-control datetimepicker-input',
            'placeholder': 'Enter Entry Time',
            "data-target": "#id_entry_time"
        }
        self.fields['stop_loss_type'].widget.attrs = {
            'class': 'form-control',
            'placeholder': 'Enter Strategy'
        }
        self.fields['stop_loss'].widget.attrs = {
            'class': 'form-control',
            'placeholder': 'Enter Strategy'
        }
        self.fields['move_sl_to_cost'].widget.attrs = {
            'class': 'form-check-input'
        }
        self.fields['active'].widget.attrs = {
            'class': 'form-check-input'
        }