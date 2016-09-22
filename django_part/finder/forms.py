from django import forms
from .models import Query


class QueryForm(forms.Form):
    query = forms.CharField(label='', max_length=150)

    class Meta:
        model = Query
        fields = ['query']

    def __init__(self, *args, **kwargs):
        super(QueryForm, self).__init__(*args, **kwargs)
        self.fields['query'].widget = forms.TextInput(attrs={
            'placeholder': 'write here',
            'type': 'search',
            'class': 'form_style',
            'name': 'query',
            'pattern': '^[А-Яа-яA-Za-z0-9\s]+$',
            'style': 'margin-left: 5px; width: 400px !important;'
        })
