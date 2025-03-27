from django import forms

class RecommendationForm(forms.Form):
    prompt = forms.CharField(
        max_length=200,
        required=True,
        label="Search movie",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Example: World War II movie',
                'id': 'prompt-input',
            }
        )
    ) 