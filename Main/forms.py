from django import forms 

TOPIC_CHOICES = (
    ('general', 'General enquiry'),
    ('bug', 'Bug report'),
    ('suggestion', 'Suggestion'),
)

class ContactForm(forms.Form):
    <ol>
        <li>topic=forms.ChoiceField(choices=TOPIC_CHOICES)</li>
        <li>message=forms.CharField(widget=forms.Textarea(), initial="Replace with your feedback")</li>
        <li>sender=forms.EmailField(required='FALSE', initial='user@example.com')</li>'
    </ol>
