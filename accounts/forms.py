from re import A
from django import forms 
from accounts.models import Account, UserProfile


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Enter password',
        'class': 'form-control',
    }))

    confirmed_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'confirm password',
        'class': 'form-control',
    }))

    class Meta:
        model = Account
        fields = ['first_name','last_name','email','phone_number']

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get('password') 
        confirmed_password = cleaned_data.get('confirmed_password') 

        if password != confirmed_password:
            
            raise forms.ValidationError(
                'please check password matching again'
            )



    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs={
                'class': 'form-control',
                'placeholder': f'Enter {field.capitalize()}'
                }

class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs={
                'class': 'form-control',
                'placeholder': f'Enter {field.capitalize()}'
                }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['address_line1', 'address_line2', 'city', 'state', 'country', 'profile_image']

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs={
                'class': 'form-control',
                'placeholder': f'Enter {field.capitalize()}'
                }