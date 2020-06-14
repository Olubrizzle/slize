from django import forms

SLIZE_CHOICES = (
    ("slize_pointfive", ".5% Slize"),
    ("slize_one", "1% Slize"),
    ("slize_five", "5% Slize"),
    ("slize_ten", "10% Slize"),
    ("slize_twenty", "20% Slize"),
    ("slize_thirty", "30% Slize"),
    ("slize_forty", "40% Slize"),
    ("slize_fifty", "50% Slize")
)

class TextInputForm(forms.Form):
    text_in = forms.CharField(widget=forms.Textarea(attrs={'cols': 140, 'rows': 20, 'style':"width:100%"}))
    slize_size = forms.ChoiceField(widget=forms.RadioSelect(), choices=SLIZE_CHOICES, required=False)
    # file_in = forms.FileField(required=True)

class AudioForm(forms.Form):
    file_in = forms.FileField(required=True)
