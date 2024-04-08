from django import forms
from .models import Post, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.utils import ErrorList
from django.contrib.auth.forms import UserChangeForm

# Profile Extras Form
class ProfilePicForm(forms.ModelForm):
    profile_image = forms.ImageField(label="Profile Picture")
    profile_bio= forms.CharField(label="Profile Bio",widget=forms.Textarea(attrs={'class':'form-control','placeholder':'Profile Bio'}))
    
    # Designating to save in profile model
    class Meta:
        model = Profile
        fields = ('profile_image',)
    

class PostForm(forms.ModelForm):
    content = forms.CharField(required=True,
            widget=forms.widgets.Textarea(
                attrs={
                    "placeholder": "Enter your post",
                    "class": "form-control"
                }
                ),
            label="",
            )
    
    class Meta:
        model = Post
        fields = ['content']  
        
class CustomErrorList(ErrorList):
    def __str__(self):
        return self.as_empty()

    def as_empty(self):
        return ''

        
class SignUpForm(UserCreationForm):
    email=forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Email Address'}))
    first_name=forms.CharField(label="", max_length=20, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}))
    last_name=forms.CharField(label="", max_length=20, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}))
    
    class Meta:
        model=User
        fields=('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs) # Intialization for SignUp Form

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'


        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'   
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'
        
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'
        
class CustomUserChangeForm(UserChangeForm):
    profile_bio = forms.CharField(label="Profile Bio", widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Profile Bio'}), required=False)
    old_password = forms.CharField(label="Old Password", widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Old Password'}), required=False)
    new_password1 = forms.CharField(label="New Password", widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New Password'}), required=False)
    new_password2 = forms.CharField(label="Confirm New Password", widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm New Password'}), required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        self.fields['profile_bio'].initial = self.instance.profile.profile_bio if hasattr(self.instance, 'profile') else ''
        
    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get("old_password")
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")
        if new_password1 and new_password2 and new_password1 != new_password2:
            self.add_error('new_password2', "The two password fields didn't match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        profile = user.profile if hasattr(user, 'profile') else None
        if profile:
            profile.profile_bio = self.cleaned_data.get('profile_bio')
        if self.cleaned_data.get('new_password1'):
            user.set_password(self.cleaned_data.get('new_password1'))
        if commit:
            user.save()
            if profile:
                profile.save()
        return user