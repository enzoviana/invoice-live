from django import forms
from django.contrib.auth.models import User
from django.forms import widgets
from .models import *
import json

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

class DateInput(forms.DateInput):
    input_type = 'date'


class UserLoginForm(forms.ModelForm):
    username = forms.CharField(
                            widget=forms.TextInput(attrs={'id': 'floatingInput', 'class': 'form-control mb-3'}),
                            required=True)
    password = forms.CharField(
                            widget=forms.PasswordInput(attrs={'id': 'floatingPassword', 'class': 'form-control mb-3'}),
                            required=True)


    class Meta:
        model=User
        fields=['username','password']



class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['clientName', 'clientLogo', 'addressLine1', 'province', 'postalCode', 'phoneNumber', 'emailAddress', 'taxNumber']



class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', 'quantity', 'price', 'currency']


class InvoiceForm(forms.ModelForm):
    THE_OPTIONS = [
    ('14 days', '14 days'),
    ('30 days', '30 days'),
    ('60 days', '60 days'),
    ]
    STATUS_OPTIONS = [
    ('CURRENT', 'CURRENT'),
    ('OVERDUE', 'OVERDUE'),
    ('PAID', 'PAID'),
    ]

    title = forms.CharField(
                    required = True,
                    label='Devis Nom ou Titre',
                    widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Enter le titre Devis'}),)
    paymentTerms = forms.ChoiceField(
                    choices = THE_OPTIONS,
                    required = True,
                    label='Selectionner option Payement  ',
                    widget=forms.Select(attrs={'class': 'form-control mb-3'}),)
    status = forms.ChoiceField(
                    choices = STATUS_OPTIONS,
                    required = True,
                    label='Changer Le Statut Du Devis',
                    widget=forms.Select(attrs={'class': 'form-control mb-3'}),)
    notes = forms.CharField(
                    required = True,
                    label='Entrer une note pour le client',
                    widget=forms.Textarea(attrs={'class': 'form-control mb-3'}))

    dueDate = forms.DateField(
                        required = True,
                        label='Date Devis',
                        widget=DateInput(attrs={'class': 'form-control mb-3'}),)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('title', css_class='form-group col-md-6'),
                Column('dueDate', css_class='form-group col-md-6'),
                css_class='form-row'),
            Row(
                Column('paymentTerms', css_class='form-group col-md-6'),
                Column('status', css_class='form-group col-md-6'),
                css_class='form-row'),
            'notes',

            Submit('submit', ' EDIT INVOICE '))

    class Meta:
        model = Invoice
        fields = ['title', 'dueDate', 'paymentTerms', 'status', 'notes']

class SettingsForm(forms.ModelForm):
    class Meta:
        model = Settings
        fields = ['clientName', 'clientLogo', 'addressLine1', 'province', 'postalCode', 'phoneNumber', 'emailAddress', 'taxNumber']

class ClientSelectForm(forms.ModelForm):

    def __init__(self,*args,**kwargs):
        self.initial_client = kwargs.pop('initial_client')
        self.CLIENT_LIST = Client.objects.all()
        self.CLIENT_CHOICES = [('-----', '--Selectionner un Client--')]


        for client in self.CLIENT_LIST:
            d_t = (client.uniqueId, client.clientName)
            self.CLIENT_CHOICES.append(d_t)


        super(ClientSelectForm,self).__init__(*args,**kwargs)

        self.fields['client'] = forms.ChoiceField(
                                        label='Selectioner un Client',
                                        choices = self.CLIENT_CHOICES,
                                        widget=forms.Select(attrs={'class': 'form-control mb-3'}),)

    class Meta:
        model = Invoice
        fields = ['client']


    def clean_client(self):
        c_client = self.cleaned_data['client']
        if c_client == '-----':
            return self.initial_client
        else:
            return Client.objects.get(uniqueId=c_client)
        
