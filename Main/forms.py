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
    ('', 'Choose a state...'),
    ('FCT', 'FCT'),
    ('Abia', 'Abia'), ('Adamawa', 'Adamawa'), ('Akwa Ibom', 'Akwa Ibom'),
    ('Anambra', 'Anambra'), ('Bauchi', 'Bauchi'), ('Bayelsa', 'Bayelsa'),
    ('Benue', 'Benue'), ('Borno', 'Borno'), ('Cross River', 'Cross River'),
    ('Delta', 'Delta'), ('Ebonyi', 'Ebonyi'), ('Edo', 'Edo'),
    ('Ekiti', 'Ekiti'), ('Enugu', 'Enugu'), ('Gombe', 'Gombe'),
    ('Imo', 'Imo'), ('Jigawa', 'Jigawa'), ('Kaduna', 'Kaduna'),
    ('Kano', 'Kano'), ('Katsina', 'Katsina'), ('Kebbi', 'Kebbi'),
    ('Kogi', 'Kogi'), ('Kwara', 'Kwara'), ('Lagos', 'Lagos'),
    ('Nasarawa', 'Nasarawa'), ('Niger', 'Niger'), ('Ogun', 'Ogun'),
    ('Ondo', 'Ondo'), ('Osun', 'Osun'), ('Oyo', 'Oyo'),
    ('Plateau', 'Plateau'), ('Rivers', 'Rivers'), ('Sokoto', 'Sokoto'),
    ('Taraba', 'Taraba'), ('Yobe', 'Yobe'), ('Zamfara', 'Zamfara'),
]

# A list of common foodstuffs to prevent invalid entries
FOODSTUFFS_CHOICES = [
    ('', 'Choose a foodstuff...'), ('Beans (brown)', 'Beans (brown)'), ('Beans (white)', 'Beans (white)'),
    ('Cassava', 'Cassava'), ('Chicken', 'Chicken'), ('Eggs', 'Eggs'), ('Fish (crayfish)', 'Fish (crayfish)'),
    ('Fish (fresh fish)', 'Fish (fresh fish)'), ('Fish (stockfish)', 'Fish (stockfish)'), ('Garri', 'Garri'),
    ('Maize', 'Maize'), ('Meat (beef)', 'Meat (beef)'), ('Meat (goat)', 'Meat (goat)'), ('Milk', 'Milk'), 
    ('Oil (palm oil)', 'Oil (palm oil)'), ('Oil (vegetable oil)', 'Oil (vegetable oil)'), ('Onions', 'Onions'),
    ('Pepper', 'Pepper'), ('Plantain', 'Plantain'), ('Potato (irish)', 'Potato (irish)'),
    ('Potato (sweet)', 'Potato (sweet)'), ('Poundo', 'Poundo'), ('Rice (foreign)', 'Rice (foreign)'),
    ('Rice (local)', 'Rice (local)'), ('Salt', 'Salt'), ('Sugar', 'Sugar'),
    ('Tomatoes', 'Tomatoes'), ('Turkey', 'Turkey'), ('Vegetables', 'Vegetables'), ('Wheat', 'Wheat'), ('Yam', 'Yam'),
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
