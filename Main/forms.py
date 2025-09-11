from django.contrib.auth.forms import UserCreationForm
from django import forms
from datetime import datetime
from .models import Price, Members
from django.core.validators import RegexValidator
from .choices import STATES_CHOICES, FOODSTUFFS_CHOICES
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

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
        required=True,
        help_text="e.g., +2348012345678"
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email', 'phone_number',)

class MemberForm(forms.ModelForm):

    phone_number_validator = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    
    company_email = forms.EmailField(
        label="Company Email",
        max_length=254,
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your company email address'
        })
    )
    
    phone = forms.CharField(
        label="Phone Number",
        max_length=15,
        validators=[phone_number_validator],
        required=True,
        help_text="e.g., +2348012345678",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'required': 'required',
            'placeholder': 'Enter your phone number'
        })
    )

    state = forms.ChoiceField(
        choices=STATES_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'required': 'required'
        })
    )
    
    class Meta:
        model = Members
        # All fields are listed here, including those defined above
        fields = ['shopname', 'ownersname', 'phone', 'company_email', 'state', 'lga', 'address', 'bio']

        # Remove 'phone', 'company_email', and 'state' from the widgets dictionary
        # as their widgets are defined explicitly above.
        widgets = {
            'shopname': forms.TextInput(attrs={
                'class': 'form-control',
                'required': 'required',
                'placeholder': 'Name of your foodstuff shop, store or mart'
            }),
            'ownersname': forms.TextInput(attrs={
                'class': 'form-control',
                'required': 'required',
                'placeholder': 'Name of the shop or store owner'
            }),
            'lga': forms.TextInput(attrs={
                'class': 'form-control',
                'required': 'required',
                'placeholder': 'Local Government where your store exists'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'required': 'required',
                'placeholder': 'Address including shop number and street or market name'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'required': 'required',
                'placeholder': 'More details about your store or shop or mart'
            }),
        }


class PurchaseForm(forms.ModelForm):
    # Redefine 'foodstuff' as a ChoiceField
    foodstuff = forms.ChoiceField(
        choices=FOODSTUFFS_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'required': 'required'
        })
    )

    # Redefine 'state' as a ChoiceField
    state = forms.ChoiceField(
        choices=STATES_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'required': 'required'
        })
    )

    class Meta:
        model = Price
        fields = ['foodstuff', 'price', 'description', 'market_store_name', 'state', 'lga']
        widgets = {
            # You can now remove 'foodstuff' and 'state' from this widget dictionary
            # as they are defined above with their new widget type
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
