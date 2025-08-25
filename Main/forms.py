from django.contrib.auth.forms import UserCreationForm
from django import forms
from datetime import datetime
from .models import Price
from django.core.validators import RegexValidator

TOPIC_CHOICES = (
    ('general', 'General enquiry'),
    ('bug', 'Bug report'),
    ('suggestion', 'Suggestion'),
)

class ContactForm(forms.Form):
    name = forms.CharField(initial='Enter your name')
    topic = forms.ChoiceField(choices=TOPIC_CHOICES)
    message = forms.CharField(widget=forms.Textarea(), initial="Replace with your feedback")
    sender = forms.EmailField(initial='user@example.com')

class CustomUserCreationForm(UserCreationForm):
    # Add phone number field with validator
    phone_number_validator = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    
    email = forms.EmailField(
        label="Email",
        max_length=254,
        required=True,
    )
    
    phone_number = forms.CharField(
        label="Phone Number",
        max_length=15,
        validators=[phone_number_validator],
        required=False,
        help_text="e.g., +2348012345678"
    )

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email', 'phone_number',)

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Price
        fields = ['foodstuff', 'price', 'description', 'market_store_name', 'state', 'lga']
        widgets = {
            'foodstuff': forms.TextInput(attrs={
                'class': 'form-control',
                'required': 'required',
                'placeholder': 'Foodstuff e.g garri, beans, yam, spaghetti'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'required': 'required',
                'placeholder': 'Price of the foodstuff you bought or sold',
                'min': '100'
            }),
            'description': forms.TextInput(attrs={
                'class': 'form-control',
                'required': 'required',
                'placeholder': 'Helpful description like brand name, quantity, or quality'
            }),
            'market_store_name': forms.TextInput(attrs={
                'class': 'form-control',
                'required': 'required',
                'placeholder': 'Name of market or store'
            }),
            'state': forms.TextInput(attrs={
                'class': 'form-control',
                'required': 'required',
                'placeholder': 'State where you made this purchase/sale'
            }),
            'lga': forms.TextInput(attrs={
                'class': 'form-control',
                'required': 'required',
                'placeholder': 'Local Government where you made this purchase/sale'
            }),
        }

class StoreForm(forms.Form):
    item_name = forms.CharField(label="Name of foodstuff listed")
    item_price = forms.IntegerField(label="Price of foodstuff being listed (per bag, carton, etc.")
    list_day = forms.DateField(initial=datetime.now)
