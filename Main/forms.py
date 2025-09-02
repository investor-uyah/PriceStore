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

# A list of Nigerian states and their acronyms (or full names)
STATES_CHOICES = [
    ('ABIA', 'Abia'), ('ADAMAWA', 'Adamawa'), ('AKWA-IBOM', 'Akwa Ibom'),
    ('ANAMBRA', 'Anambra'), ('BAUCHI', 'Bauchi'), ('BAYELSA', 'Bayelsa'),
    ('BENUE', 'Benue'), ('BORNO', 'Borno'), ('CROSS-RIVER', 'Cross River'),
    ('DELTA', 'Delta'), ('EBONYI', 'Ebonyi'), ('EDO', 'Edo'),
    ('EKITI', 'Ekiti'), ('ENUGU', 'Enugu'), ('GOMBE', 'Gombe'),
    ('IMO', 'Imo'), ('JIGAWA', 'Jigawa'), ('KADUNA', 'Kaduna'),
    ('KANO', 'Kano'), ('KATSINA', 'Katsina'), ('KEBBI', 'Kebbi'),
    ('KOGI', 'Kogi'), ('KWARA', 'Kwara'), ('LAGOS', 'Lagos'),
    ('NASARAWA', 'Nasarawa'), ('NIGER', 'Niger'), ('OGUN', 'Ogun'),
    ('ONDO', 'Ondo'), ('OSUN', 'Osun'), ('OYO', 'Oyo'),
    ('PLATEAU', 'Plateau'), ('RIVERS', 'Rivers'), ('SOKOTO', 'Sokoto'),
    ('TARABA', 'Taraba'), ('YOBE', 'Yobe'), ('ZAMFARA', 'Zamfara'),
    ('FCT', 'Federal Capital Territory')
]

# A list of common foodstuffs to prevent invalid entries
FOODSTUFFS_CHOICES = [
    ('RICE', 'Rice'), ('BEANS', 'Beans'), ('YAM', 'Yam'),
    ('GARRI', 'Garri'), ('PLANTAIN', 'Plantain'), ('CASSAVA', 'Cassava'),
    ('WHEAT', 'Wheat'), ('MAIZE', 'Maize'), ('VEGETABLES', 'Vegetables'),
    ('TOMATOES', 'Tomatoes'), ('PEPPER', 'Pepper'), ('ONIONS', 'Onions'),
    ('FISH', 'Fish'), ('MEAT', 'Meat'), ('CHICKEN', 'Chicken'),
    ('EGGS', 'Eggs'), ('SALT', 'Salt'), ('SUGAR', 'Sugar'),
    ('OIL', 'Oil'), ('MILK', 'Milk'),
]

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
