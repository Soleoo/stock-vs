from django import forms
from .models import User

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    full_name = forms.CharField(label='Full Name', widget=forms.TextInput(attrs={'class': 'form-control'}))
    face_image = forms.ImageField(label='Face Image', required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, label='Role', widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'full_name', 'phone_number', 'password', 'role', 'face_image')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user