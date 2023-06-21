from django import forms
from .models import Task
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

User = get_user_model()


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "due_date", "priority", "completed","user"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "due_date": forms.DateInput(attrs={"class": "form-control"}),
            "priority": forms.Select(attrs={"class": "form-control"}),
            "completed": forms.CheckboxInput(),
            "user":forms.Select(attrs={"class": "form-control"}),
        }


class CustomRegistrationForm(UserCreationForm):
    
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "First Name"}
        ),
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Last Name"}
        ),
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Email"}
        ),
    )
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Username"}
        ),
    )
    mobile = forms.IntegerField(
        max_value=9999999999,
        min_value=1000000000,
        required=True,
        widget=forms.TextInput(
        attrs={"class": "form-control", "placeholder": "Mobile number"}
    ),
    )
    pincode = forms.IntegerField(
        max_value=999999,
        min_value=100000,
        required=True,
        widget=forms.TextInput(
        attrs={"class": "form-control", "placeholder": "Pincode"}
    ),
    )
    address = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(
        attrs={"class": "form-control", "placeholder": "Address"}
    ),
    )
    password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
        attrs={"class": "form-control", "placeholder": "Password"}
    ),
    )
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
        attrs={"class": "form-control", "placeholder": "Confirm Password"}
    ),
    )
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "mobile",
            "email",
            "pincode",
            "address",
            "password1",
            "password2",
        ]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].validators = []


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
