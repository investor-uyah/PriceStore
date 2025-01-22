from django import forms 
from datetime import datetime
from .models import Price

TOPIC_CHOICES = (
    ('general', 'General enquiry'),
    ('bug', 'Bug report'),
    ('suggestion', 'Suggestion'),
)

class ContactForm(forms.Form):
    name=forms.CharField(initial='Enter your name'),
    topic=forms.ChoiceField(choices=TOPIC_CHOICES),
    message=forms.CharField(widget=forms.Textarea(), initial="Replace with your feedback"),
    sender=forms.EmailField(initial='user@example.com'),

# class PurchaseForm(forms.Form):
    food_name=forms.CharField(label="Name of foodstuff you purchased"), 
    price=forms.IntegerField(label="Price"),
    day=forms.DateField(label="day of purchase", initial=datetime.now),

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Price
        fields = ['foodstuff', 'price', 'description', 'author']

class StoreForm(forms.Form):
    item_name=forms.CharField(label="Name of foodstuff listed"),
    item_price=forms.IntegerField(label="Price of foodstuff being listed (per bag, carton, etc."),
    list_day=forms.DateField(initial=datetime.now),
